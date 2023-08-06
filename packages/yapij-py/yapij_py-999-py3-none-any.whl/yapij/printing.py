"""Creates modified versions of most common functions that go to stdout/stderr: print, Exception, help.

For each type of object, it packages them neatly into msgpack bytes for stdout.
"""
import sys
import traceback
import copy
import inspect

from msgpack import packb

try:
  from . import packers
  from .config import use_bin_type
except (ModuleNotFoundError, ImportError):
  import packers
  from config import use_bin_type

__all__ = ['get_uid_out']


def get_uid_out(uid):
  def print_modified(
    *objects, sep=' ', end='\n', file=sys.stdout, flush=False
  ):

    willSep = sep != '' and len(objects) > 1

    for obj in objects:
      d = packers.pack_explicit(obj)

      sys.stdout.write(packb(d(uid, obj), use_bin_type=True))
      if willSep:
        sys.stdout.write(
          packb(packers.pack_sep(uid, sep), use_bin_type=use_bin_type)
        )
    sys.stdout.write(
      packb(packers.pack_end(uid, end), use_bin_type=use_bin_type)
    )
    if flush:
      sys.stdout.flush()

  def raise_modified(e, sys_stdout=sys.stdout):

    sys_stdout.write(
      packb(packers.pack_exception(uid, e), use_bin_type=use_bin_type)
    )
    sys.stdout.write(
      packb(packers.pack_end(uid, '\n'), use_bin_type=use_bin_type)
    )
    sys_stdout.flush()

  def help_modified(d):
    sys.stdout.write(packb(packers.pack_docstring(uid, d)))
    sys.stdout.write(
      packb(packers.pack_end(uid, '\n'), use_bin_type=use_bin_type)
    )
    sys.stdout.flush()

  def warning_modified(d):
    sys.stdout.write(packb(packers.pack_warning(uid, d)))
    sys.stdout.write(
      packb(packers.pack_end(uid, '\n'), use_bin_type=use_bin_type)
    )
    sys.stdout.flush()

  return print_modified, raise_modified, help_modified, warning_modified
