import os
import time
import typing
import re
from subprocess import call
import sys
import keyword
import runpy
import asyncio
from concurrent.futures._base import Future
import queue
import zmq

try:
  from .threading2 import Thread2
  from .exceptions import InterruptExecution, YapijError
  from . import status_msg
  from .context import create_catch_output
except (ModuleNotFoundError, ImportError):
  from threading2 import Thread2
  from exceptions import InterruptExecution, YapijError
  import status_msg
  from context import create_catch_output

keyword2 = keyword.kwlist.copy()
keyword2.remove('True')
keyword2.remove('False')
keyword2.append('print')

__all__ = ['Session']


class Session(object):
  """Operates as a queue for running interpreter commands.

  Attributes:
      done_callback_passed (typing.Callable[[Future], None]): Description
      env (dict): Description
      is_running (bool): Description
      q (queue.Queue): Description
      loop (asyncio.AbstractEventLoop): Description
  """

  def __init__(
    self, worker: Thread2, loop: asyncio.AbstractEventLoop,
    done_callback: typing.Callable[[Future], None],
    get_env: typing.Callable[[], dict], pub: zmq.Socket, PUB_TOPIC: bytes,
    PUB_STATUS: bytes
  ):

    self.worker = worker
    self.loop = loop
    self.done_callback_passed = done_callback
    self.get_env = get_env

    self.pub = pub
    self.PUB_STATUS = PUB_STATUS
    self.catch_output, _ = create_catch_output(pub, PUB_TOPIC)

    self.q = queue.Queue()
    self.is_running = False

  def interrupt(self):
    self.q.empty()
    self.worker.raise_exc(InterruptExecution)

  def run(self, uid: bytes, cmd: str):
    cmds = cmd.rsplit('\n', 1)
    if len(cmds) > 1:
      if self._can_be_printed(cmds[1]):
        cmds[1] = 'print({})'.format(cmds[1])
      cmd = '\n'.join(cmds)
    else:
      cmd = cmds[0]
      if self._can_be_printed(cmd):
        cmd = 'print({})'.format(cmd)

    self.q.put(('code', cmd, uid))

    self.pub.send_multipart([self.PUB_STATUS, uid, status_msg.QUEUED_EXEC])

    if not self.is_running:
      self.check_queue()

  def run_file(self, args: dict):
    self.q.put(('file', args))
    if not self.is_running:
      self.check_queue()

  def check_queue(self):
    try:
      task = self.q.get_nowait()
      self.pub.send_multipart(
        [self.PUB_STATUS, task[2], status_msg.STARTED_EXEC]
      )
      if task[0] == 'file':

        # Append env only when ready to call file (otherwise, will operate on an old environment)
        if not task[1]['init_globals']:
          task[1]['init_globals'] = self.get_env()

        fut = asyncio.run_coroutine_threadsafe(
          exec_file(self.catch_output, task[2], task[1]), self.loop
        )
        self.is_running = True
        fut.add_done_callback(self._done_callback)
      elif task[0] == 'code':
        env = self.get_env()
        t = task[1]
        fut = asyncio.run_coroutine_threadsafe(
          exec_one_command(self.catch_output, task[2], t, env), self.loop
        )
        self.is_running = True
        fut.add_done_callback(self._done_callback)
      else:
        raise YapijError(
          f'Task type "{task[0]}" not recognized! File a bug report please.'
        )

    except queue.Empty:
      pass

  def _done_callback(self, fut: Future) -> None:

    status = fut.result()['status']
    self.done_callback_passed(fut)

    self.is_running = False
    self.pub.send_multipart([self.PUB_STATUS, fut.result()['uid'], status])
    if fut.result()['error']:
      with self.catch_output(fut.result()['uid']):
        raise fut.result()['error']

    self.check_queue()

  @staticmethod
  def _can_be_printed(cmd) -> bool:
    s_cmd = re.split(r'\(|\s', cmd)[0]
    return not cmd.startswith(r'\s') and (
      ('=' not in cmd) or re.match(r'.*(\!=|==).*', cmd)
    ) and s_cmd not in keyword2


async def exec_one_command(context, uid: bytes, cmd, env: dict):
  """Executes arbitrary code."""
  status = b'-5'
  error = None
  with context(uid):
    try:
      code = compile(cmd, '<str>', 'exec')
      exec(code, {}, env)
      status = status_msg.FINISHED_EXEC
      error = None
    except InterruptExecution as e:
      status = status_msg.INTERRUPT_EXEC
      error = e
    except Exception as e:
      status = status_msg.ERROR_EXEC
      error = e
    finally:
      return {'uid': uid, 'env': env, 'status': status, 'error': error}


async def exec_file(context, uid: bytes, args: dict):
  """Executes arbitrary code."""
  with context(uid):
    try:
      status = 0
      env = await runpy.run_path(**args)
      status += 1
    except InterruptExecution:
      status -= 2
      raise InterruptedError
    except BaseException as e:
      status -= 1
      raise e
    finally:
      return {'uid': uid, 'env': env, 'status': status}
