import dill
import warnings
import os
import uuid
import io
import sys
import hmac
import hashlib
from datetime import datetime
from random import randint
from getpass import getuser

__all__ = ['WorkspaceManager']


class WorkspaceManager(object):
  """Manages python workspaces.
  Attributes:
      date_created (TYPE): Description
      env (TYPE): Description
      file_metadata (TYPE): Description
      filename (TYPE): Description
      user (TYPE): Description
      user_id (TYPE): Description
      uuid (TYPE): Description
  """

  INIT_PYTHON_KEYS = {
    # '__name__', '__doc__', '__package__', '__loader__', '__spec__',
    # '__annotations__', '__builtins__'
  }

  def __init__(
    self, user: [None, str] = None, filename: [None, str] = None
  ):

    self.user = user if user else getuser()
    self.login = getuser()
    self.uuid = uuid.getnode()

    # self.new(filename)

  def new(self, filename: [str, None] = None):

    self._set_filename(filename)
    self.env = self._init_globals()
    self.file_metadata = {
      'info':
        {
          'creator_user': self.user,
          'creator_login': self.login,
          'creator_uuid': self.uuid,
          'date_created': datetime.now(),
          'filename': self.filename,
          'pwd': os.getcwd()
        },
      'edit_history': []
    }
    self._add_edit_history_log('create')

  def save(self) -> None:
    self._save(self.filename)
    self._add_edit_history_log('save')

  def load(self, filename: str) -> bool:
    # Make a temporary save of current workspace in case
    tmp = self._create_tempfile(local=False)
    self._save(tmp)
    old_filename = self.filename

    # Check to make sure that file exists and is of proper type.
    filename = os.path.abspath(filename)
    if not os.path.isfile(filename):
      raise ValueError(
        'Specified file `{}` does not exist!'.format(filename)
      )
    filename = self._set_filename(filename, inplace=False)

    try:
      ws = self._load(filename)

      eh = ws['file_metadata']['edit_history'][-1]

      self.env = ws['env']
      self.file_metadata = ws['file_metadata']
      self.filename = filename
      self._add_edit_history_log('load')
    except Exception as e:
      ws = self._load(tmp)
      self.env = ws['env']
      self.file_metadata = ws['file_metadata']
      self.filename = old_filename
      os.remove(tmp)
      raise e

    return None

  def delete(self, filename: [None, str] = None) -> None:
    if not filename or filename == self.filename:
      filename = self.filename
      self.new(filename)
      if not os.path.isfile(filename):
        return None

    filename = os.path.abspath(filename)
    ft = os.path.splitext(filename)
    if not os.path.isfile(filename):
      raise ValueError(
        'Cannot delete: Specified file `{}` does not exist!'.
        format(filename)
      )
    elif len(ft) != 2:
      raise ValueError('Cannot delete: Must be a `.gtmm` file.')
    elif ft[1] != '.gtmm':
      raise ValueError('Cannot delete: Must be a `.gtmm` file.')
    os.remove(filename)

  def copy(self, filename: [None, str] = None) -> None:
    old_filename = filename

    if filename is None:
      ft = os.path.splitext(filename)
      filename = ft[0] + ' (copy)' + ft[1]

    try:
      self._set_filename(filename)
      self._save(filename)
      self._add_edit_history_log('copy')
    except Exception as e:
      self.filename = old_filename
      raise e

  def rename(self, filename: str) -> None:
    old_filename = self.filename

    try:
      self._set_filename(filename)
      self._save(filename)
      if os.path.isfile(old_filename):
        os.remove(old_filename)
      self._add_edit_history_log('rename')
    except Exception as e:
      self.filename = old_filename
      if os.path.isfile(filename):
        os.remove(filename)
      raise e

  def reset(self):
    self.env = self._init_globals()
    self._add_edit_history_log('reset')

  def who(self):
    total_size = 0
    n_objects = 0
    fmt_str = '{:20.20s}  {:20.20s}  {:>12.3f}'
    print('{:20s}  {:20s}  {:>15s}'.format('Object', 'Type', 'Size (kb)'))
    print('-' * 59)
    for k, v in self.env.items():
      if repr(type(v)) == "<class 'numpy.ndarray'>":
        size = v.nbytes / 1000
      else:
        size = v.__sizeof__() / 1000
      total_size += size
      n_objects += 1
      print(fmt_str.format(k, str(type(v)).split('\'')[1], size))
    print('-' * 59)
    print(
      '# Objects: {:<12d}\tTotal Size (kb): {:<12.3f}'.format(
        n_objects, total_size
      )
    )

  def workspace_info(self):

    n_objects, total_size = 0, 0

    def _inner(k, v):
      if repr(type(v)) == "<class 'numpy.ndarray'>":
        size = v.nbytes / 1000
      else:
        size = v.__sizeof__() / 1000
      total_size += size
      n_objects += 1
      return {"var": k, "type": str(type(v)).split('\'')[1], "size": size}

    env = [_inner(k, v) for k, v in self.env.items()]
    return {
      "env": env,
      "stats": {
        "n_objects": n_objects,
        "total_size": total_size
      },
      "metadata": self.file_metadata
    }

  def _save(self, filename: str):
    pickled_data = dill.dumps(
      {
        'env': self.env,
        'file_metadata': self.file_metadata
      }
    )

    # Encryption
    digest = hmac.new(b'shared-key', pickled_data,
                      hashlib.sha1).hexdigest()

    header = bytes('{:s}$$gtmm%gtmm$$'.format(digest), 'utf-8')
    data = header + pickled_data
    with open(filename, 'wb') as file:
      file.write(data)

  def _load(self, filename: str):
    # Decryption
    with open(filename, 'rb') as file:
      data = file.read()
    recvd_digest, pickled_data = data.split(b'$$gtmm%gtmm$$')

    new_digest = hmac.new(b'shared-key', pickled_data,
                          hashlib.sha1).hexdigest()

    if new_digest != recvd_digest.decode('utf-8'):
      raise IOError()

    return dill.loads(pickled_data)

  def _init_globals(self) -> dict:
    """When need to re-initialize environment will get only objects in globals() that appear in preset list, which is the initial globals() state on python 3.6.3 startup.
    Returns:
        dict: Dictionary of globals widdled down to size.
    """
    g = globals()
    return {k: g[k] for k in g.keys() & self.INIT_PYTHON_KEYS}

  def _add_edit_history_log(self, modification_type: str):
    self.file_metadata['info']['filename'] = self.filename
    self.file_metadata['info']['pwd'] = os.getcwd()
    self.file_metadata['edit_history'].append(
      {
        "filename": self.filename,
        "modifier_user": self.user,
        "modifier_login": self.login,
        "modifier_uuid": self.uuid,
        "os": sys.platform,
        "date_modified": datetime.now(),
        "modification_type": modification_type
      }
    )

  def _set_filename(
    self, filename: [str, None], local: bool = False, inplace: bool = True
  ):
    if not filename:
      return self._create_tempfile(local)

    filename = os.path.abspath(filename)
    ft = os.path.splitext(filename)
    if len(ft) != 2:
      raise ValueError('Must use extension of type!')
    elif not os.path.isdir(os.path.split(filename)[0]):
      raise ValueError(
        'Path `{}` does not exist!'.format(os.path.split(filename)[0])
      )
    elif ft[1] != '.gtmm':
      raise ValueError(
        f'Must use a `.gtmm` filename! Received: {filename}'
      )
    elif inplace:
      self.filename = filename
    return filename

  def _create_tempfile(self, local: bool = True):
    now = datetime.now()
    fn = 'untitled-{:02d}{:02d}{:02d}-{:02d}{:02d}{:02d}.gtmm'.format(
      now.month, now.day, now.year, now.hour, now.minute, now.second
    )
    if local:
      fd = os.getcwd()
    else:
      from tempfile import gettempdir
      fd = gettempdir()
    self.filename = os.path.join(fd, fn)
    return self.filename

  def __str__(self):
    out = 'WorkspaceManager:'
    if len(self.file_metadata['edit_history']) > 0:
      info = self.file_metadata['info']
      eh = self.file_metadata['edit_history'][-1]
      out += '\nFilename: {}'.format(eh['filename'])

      out += '\n  Created:\n     Date:{}\n  Creator:\n     Name: {}\n    Login: {}\n     UUID: {}'.format(
        info['date_created'], info['creator_user'], info['creator_login'],
        info['creator_uuid']
      )
      out += '\n  Modified:\n     Date:{}\n  Modifier:\n     Name: {}\n    Login: {}\n     UUID: {}'.format(
        eh['date_modified'], eh['modifier_user'], eh['modifier_login'],
        eh['modifier_uuid']
      )
      if eh['modification_type'] == 'create':
        out += '\n   [FILE NOT YET SAVED.]'

    else:
      out += '\n   [No workspace created or saved.]'

    return out
