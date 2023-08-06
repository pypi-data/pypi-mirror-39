import sys
import traceback
import io
import inspect
import types


class TestClass:
  pass


def check_inspectable(d):
  return isinstance(
    d, (
      types.ModuleType, types.TracebackType, types.FunctionType,
      types.MethodType, types.CodeType, types.FrameType, TestClass
    )
  )


def fmt_exception(e):
  exc_type, exc_value, exc_tb = sys.exc_info()
  tb = traceback.format_exception(exc_type, exc_value, exc_tb)

  return {
    'type': str(exc_type).split('\'')[1],
    'tb': ''.join(tb),
    'args': e.args,
    'lineno': exc_tb.tb_lineno
  }


def fmt_warning(w):
  return {
    'type': str(w.category).split('\'')[1],
    'file': str(w.file),
    'lineno': w.lineno,
    'msg': str(w.message),
    'source': str(w.source)
  }


def fmt_docstring(d):

  out = {
    'type': str(type(d)).split('\'')[1],
    'docstring': getattr(d, '__doc__', '')
  }

  if hasattr(d, '__name__'):
    out['name'] = getattr(d, '__name__', '')
  elif hasattr(d, '__class__'
               ) and hasattr(getattr(d, '__class__'), '__name__'):
    out['name'] = getattr(getattr(d, '__class__'), '__name__', '')
  else:
    out['name'] = '[Name Unknown]'

  if inspect.isfunction(d) or inspect.isclass(d):
    out['signature'] = '{}{}'.format(
      out['name'],
      inspect.signature(d).__str__()
    )

  if inspect.ismodule(d) or inspect.isclass(d):
    out['dir'] = dir(d)

  if not inspect.ismodule(d):

    out['module'] = getattr(inspect.getmodule(d), '__package__', '')
    if out['module'] not in ['builtins', '__main__']:
      if check_inspectable(d):
        out['file'] = inspect.getsourcefile(d)
      elif hasattr(d, '__class__'
                   ) and hasattr(getattr(d, '__class__'), '__name__'):
        out['file'] = inspect.getsourcefile(d.__class__)

  return out


def fmt_figure(d):

  img = io.StringIO()
  d.savefig(img, format='svg')
  img.seek(0)

  return ''.join(img.readlines())
