import sys
import contextlib
import warnings
import copy

try:
  from .ZMQIOWrapper import ZMQIOWrapper
  from .printing import get_uid_out
except (ModuleNotFoundError, ImportError):
  from ZMQIOWrapper import ZMQIOWrapper
  from printing import get_uid_out

__all__ = ['catch_output']

# Original
stdout_original = sys.stdout
stderr_original = sys.stderr
print_original = copy.copy(__builtins__['print'])


def create_catch_output(pub, topic):

  stdout_modified = ZMQIOWrapper(
    buf=sys.stdout.buffer, pub=pub, topic=topic
  )

  @contextlib.contextmanager
  def catch_output_outer():
    try:
      sys.stdout = stdout_modified
      yield
    finally:
      sys.stdout = stdout_original

  @contextlib.contextmanager
  def catch_output(uid):
    print_mod, raise_mod, help_mod, warning_mod = get_uid_out(uid)

    try:
      sys.stdout = stdout_modified
      __builtins__['print'] = print_mod
      __builtins__['help'] = help_mod
      with warnings.catch_warnings(record=True) as w:
        yield
    except BaseException as e:
      raise_mod(e, stdout_modified)
    finally:
      for wi in w:
        warning_mod(wi)

      __builtins__['help'] = help_mod
      __builtins__['print'] = print_original
      sys.stdout = stdout_original

  return catch_output, catch_output_outer


# @contextlib.contextmanager
# def catch_magic():
#   try:
#     o_print = copy.copy(__builtins__['print'])
#     __builtins__['print'] = print_magic
#     yield
#   except BaseException as e:
#     raise_magic(e)
#   finally:
#     __builtins__['print'] = o_print
