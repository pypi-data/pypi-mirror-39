import shlex
import typing
import re
from subprocess import call
import sys
import os
from concurrent.futures._base import Future
import asyncio
import warnings
import zmq
import keyword

try:
  from .magic import YapijMagicFunction, register_magic, MagicDoesNotExistError
  from .config import encoding
  from .WorkspaceManager import WorkspaceManager
  from .config import encoding
  from .session import Session
  from .threading2 import Thread2
  from .exceptions import YapijError
  from . import status_msg
  from .context import create_catch_output
except (ModuleNotFoundError, ImportError):
  from magic import YapijMagicFunction, register_magic, MagicDoesNotExistError
  from config import encoding
  from WorkspaceManager import WorkspaceManager
  from config import encoding
  from session import Session
  from threading2 import Thread2
  from exceptions import YapijError
  import status_msg
  from context import create_catch_output

keyword2 = keyword.kwlist.copy()
keyword2.remove('True')
keyword2.remove('False')
keyword2.append('print')

__all__ = ['BaseManager', 'ZmqManager']


class BaseManager(object):
  """Abstract command class containing boilerplate/routers for an interface similar to built-in class `cmd.Cmd`.

  To use, create a sub-class that adds magics with the `@register_magic` decorator.

  Attributes:
      opts (TYPE): Description
      workspace (TYPE): Description
  """

  def __init__(
    self,
    init_filename: [str, None] = None,
    user: [str, None] = None,
    startup_script: [str, None] = None,
    cd: [str, None] = None
  ):
    self.workspace = WorkspaceManager(user=user)
    self._sts = startup_script

    if cd:
      cd = os.path.abspath(cd)
      if os.path.isdir(cd):
        os.chdir(cd)
      else:
        warnings.warn(
          f'\nInitial directory path\n\n\t`{cd}`\n\nis invalid.\nMaintaining current working directory:\n\n\t`{os.getcwd()}`\n\nYou can change the directory path by calling:\n\n\t%cd [path]'
        )

    if init_filename and os.path.exists(init_filename):
      self.workspace.load(init_filename)
    else:
      self.workspace.new(init_filename)

  def __call__(self, args: [str, bytes]):

    # Handling of args prior to command being issued
    args = self.precmd(args)
    # Routing of command to different places
    self._call_route(args)
    # What is done to args after command is complete
    self.postcmd(args)

  def precmd(self, args: [str, bytes]):
    if isinstance(args, bytes):
      args = args.decode(encoding)

    # Replace help hook with `help()` built-in. If a magic, be sure to call the magi-fied version instead (line 2).
    args = re.sub(r'(\n|^)\?(.*)|(.*)\?$', '\\1help(\\2\\3)', args)
    args = re.sub(r'(\n|^)help\(\%(.*)\)', '\\1%help %\\2', args)
    return args

  def postcmd(self, args: str):
    return args

  def _call_route(self, args):
    if args.startswith('%'):
      self._call_magic(args)
    elif args.startswith('!'):
      self.do_shell(args)
    else:
      self.do_exec(uid, args)

  def _call_magic(self, args):
    if re.search(r'\n', args):
      args = list(shlex.shlex(args, punctuation_chars=True))
      # Handles case where newline is within an argument
      if not any([re.search(r'\n', a) for a in args]):
        raise SyntaxError('Line magic only works one line at a time!')
    else:
      args = list(shlex.shlex(args, punctuation_chars=True))
    cmd = getattr(self, 'mgc_' + args[1], None)
    if cmd and isinstance(cmd, YapijMagicFunction):
      cmd(self, args[2:])
    else:
      raise MagicDoesNotExistError(args[1], args[0])

  def _check_permissions(self, force: bool):
    if force:
      return True
    else:
      raise PermissionError(
        "Cannot excecute command in untrusted environments! If you know that the script is safe, either run with `--force=True` flag or call `%trust True` then try repeating this command."
      )

  @staticmethod
  def _can_be_printed(cmd) -> bool:
    s_cmd = re.split(r'\(|\s', cmd)[0]
    return not cmd.startswith(' ') and not cmd.startswith('\t') and (
      ('=' not in cmd) or re.match(r'.*(\!=|==).*', cmd)
    ) and s_cmd not in keyword2

  def do_exec(self, args):
    cmds = args.rsplit('\n', 1)
    if len(cmds) > 1:
      if self._can_be_printed(cmds[-1]):
        cmds[-1] = 'print({})'.format(cmds[-1])
      cmd = '\n'.join(cmds)
    else:
      cmd = cmds[0]
      if self._can_be_printed(cmd):
        cmd = 'print({})'.format(cmd)
    code = compile(cmd, '<str>', 'exec')
    exec(code, self.workspace.env)

  @register_magic(prefix='!')
  def do_shell(
    self,
    args: str,
    force: bool = False,
    stdin=None,
    stdout=None,
    stderr=None,
    shell=False,
    cwd=None,
    timeout=None
  ):
    self._check_permissions(force)
    check_call(
      args,
      stdin=stdin,
      stdout=stdout,
      stderr=stderr,
      shell=shell,
      cwd=cwd,
      timeout=timeout
    )

  def do_init(self):
    """Run any startup scripts. Segmented out so that only calls when, e.g. thread is started.
    """
    if self._sts:
      self.do_exec(self._sts)


class ZmqManager(BaseManager):
  def __init__(
    self,
    worker: Thread2,
    loop: asyncio.AbstractEventLoop,
    pub: zmq.Socket,
    PUB_TOPIC: bytes,
    PUB_STATUS: bytes,
    init_filename: [str, None] = None,
    user: [str, None] = None,
    startup_script: [str, None] = None,
    cd: [str, None] = None
  ):
    """
    Args:
        init_filename (str, None, optional): Description
        user (str, None, optional): Description
        never_trust (bool, optional): Description
        startup_script (str, None, optional): Description
    """
    super().__init__(init_filename, user, startup_script, cd)
    self.pub = pub
    self.PUB_STATUS = PUB_STATUS
    self.catch_output, _ = create_catch_output(pub, PUB_TOPIC)

    self.session = Session(
      worker, loop, self._done_callback, self._get_env, self.pub,
      PUB_TOPIC, self.PUB_STATUS
    )

  def __call__(self, uid: bytes, args: [str, bytes]):
    self.pub.send_multipart([self.PUB_STATUS, uid, status_msg.RECEIVED])
    # Handling of args prior to command being issued
    args = self.precmd(args)
    # Routing of command to different places
    self._call_route(uid, args)
    # NOTE: Remove `postcmd` because doesn't do anything right now. Just like the pattern.

  def _call_route(self, uid: bytes, args: [str, bytes]):
    if args.startswith('%'):
      self._call_magic(uid, args)
    elif args.startswith('!'):
      self.do_shell(uid, args)
    else:
      self.do_exec(uid, args)

  def _call_magic(self, uid: bytes, args: str):
    self.pub.send_multipart(
      [self.PUB_STATUS, uid, status_msg.STARTED_MAGIC]
    )
    with self.catch_output(uid):
      super()._call_magic(args)
    self.pub.send_multipart(
      [self.PUB_STATUS, uid, status_msg.FINISHED_MAGIC]
    )

  @register_magic()
  def mgc_help(self, prefix, mgc):
    """One of many ways to get help. This is probably the worst way to do it as a user at the moment.

    NOTE: You can get help on _any_ method by using `?`. For example: `?print` or even `?%run`.

    NOTE: Currently only works for magic commands

    TODO: Add support for this command for regular environment variables (i.e. divert to exec if magic not found)

    Args:
        prefix (TYPE): Description
        mgc (TYPE): Description

    Raises:
        MagicDoesNotExistError: Description
    """
    cmd = getattr(self, 'mgc_' + mgc, None)
    if cmd and isinstance(cmd, YapijMagicFunction):
      help(cmd)
    else:
      raise MagicDoesNotExistError(mgc, prefix, '%help Failure')

  @register_magic()
  def mgc_quit(self, force: bool):

    raise NotImplementedError(
      'Must add handling for stdin before this can be done via python. Instead, implement in JS.'
    )

  @register_magic()
  def mgc_restart(self, force: bool):

    raise NotImplementedError(
      'Must add handling for stdin before this can be done via python. Instead, implement in JS.'
    )

  @register_magic()
  def mgc_interrupt(self):
    """Interrupt execution of threads.
    """
    self.session.interrupt()

  @register_magic()
  def mgc_pwd(self):
    """Get the current working directory
    """
    print('\'{}\''.format(os.getcwd()))

  @register_magic()
  def mgc_cd(self, path):
    """Set the current working directory
    """
    cd = os.path.abspath(cd)
    if os.path.isdir(cd):
      os.chdir(cd)
    else:
      raise YapijError(
        f'\nInitial directory path\n\n\t`{cd}`\n\nis invalid.\nMaintaining current working directory:\n\n\t`{os.getcwd()}`'
      )
    print('\'{}\''.format(os.getcwd()))

  @register_magic()
  def mgc_save(self):
    self.workspace.save()

  @register_magic()
  def mgc_load(self, filename: str):
    self.session.interrupt()
    self.workspace.load(filename)

  @register_magic()
  def mgc_rename(self, filename: str):
    self.workspace.rename(filename)

  @register_magic()
  def mgc_reset(self):
    self.session.interrupt()
    self.workspace.reset()

  @register_magic()
  def mgc_copy(self, filename: [str, None]):
    self.workspace.copy(filename)

  @register_magic()
  def mgc_delete(self, filename: [str, None]):
    self.workspace.delete(filename)

  @register_magic()
  def mgc_new(self, filename: [str, None]):
    self.session.interrupt()
    self.workspace.new(filename)

  @register_magic()
  def mgc_who(self, about: [str, None] = None):
    """
    Get information about different kernel objects.

    Example:

      %who workspace # Workspace info
      %who env       # Session Environment info
      %who           # Defaults to info about environment

    Args:
        about (str): Either `workspace` or `process`
    """
    if about:
      about = about.lower()
    else:
      about = 'env'

    if about == 'env':
      self.workspace.who()
    elif about == 'workspace':
      print(self.workspace)
    else:
      raise ValueError('No info available for `{}`'.format(about))

  @register_magic()
  def mgc_workspace_info(self):
    print(self.workspace.workspace_info())

  @register_magic()
  def mgc_run(
    self,
    filename: str,
    g: [dict, None] = None,
    n: [str, None] = '__main__',
    o: [bool] = True
  ):
    p = os.path.abspath(filename)
    if not os.path.isfile(p):
      raise FileNotFoundError('Could not find `{}`'.format(p))
    elif not os.path.splitext(p)[1] != b'.py':
      raise ValueError(
        'Must be a python (i.e. `.py` file). Received file with extension: `{}`'
        .format(os.path.splitext(p)[1])
      )
    self.session.run_file(
      {
        'file_path': p,
        'init_globals': g,
        'run_name': n,
        'overwrite': o
      }
    )

  @register_magic()
  def mgc_load_ext(self, magic: YapijMagicFunction, force: bool = False):
    self._check_permissions(force)
    setattr(self, 'mgc_' + magic.__name__, magic)

  def do_exec(self, uid: bytes, args: [bytes, str]):
    self.session.run(uid, args)

  def _done_callback(self, fut: Future):
    self.workspace.env = fut.result()['env']

  def _get_env(self):
    return self.workspace.env