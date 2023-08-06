"""Magic handlers:

Gameplan:

- Add `register_magic` decorators to files
- Use shlex.shlex to parse the incoming commands
- Save magics to a congig file.

Attributes:
    ex (TYPE): Description
    func (TYPE): Description
    s (TYPE): Description
"""
import shlex
import argparse
import inspect
import typing
import importlib.util
import functools


class MagicDoesNotExistError(Exception):
  def __init__(self, magic_name: str, prefix: str = '%', *args, **kwargs):
    msg = 'Magic `{}{}` not found!'.format(prefix, magic_name)
    Exception.__init__(self, msg, *args, **kwargs)


class YapijMagicFunction(object):
  def __init__(
    self,
    name: [str, None],
    func: typing.Callable,
    parser_opts: dict = {},
    arg_opts: dict = {},
    is_method: bool = True,
    prefix: str = '%'
  ):
    self.name = name
    self.func = func
    self._parser = None
    self._parser_opts = parser_opts
    self._arg_opts = arg_opts
    self.is_method = is_method
    self.prefix = prefix

    if name.startswith('do_'):
      self.name = name.split('do_')[-1]

  @property
  def parser(self):
    return self._parser if self._parser else self._make_parser()

  def _parse_param(self, nm, arg):
    out = {'metavar': nm.upper()}

    if arg.default == inspect._empty:
      out_name = nm
    else:
      out_name = '--{}'.format(nm)
      out['default'] = arg.default

    if arg.annotation != inspect._empty:
      if type(arg.annotation) is type:
        # NOTE: Only add if one type is passed.
        out['type'] = arg.annotation

    return out_name, {**out, **self._arg_opts.pop(nm, {})}

  def _make_parser(self):
    p = argparse.ArgumentParser(
      **{
        **{
          'prog': '%{}'.format(self.name),
          'add_help': False,
          'description': self.func.__doc__
        },
        **self._parser_opts
      }
    )

    n_args = 0
    for ii, (k, v) in enumerate(
      inspect.signature(self.func).parameters.items()
    ):
      if ii == 0 and self.is_method and k == 'self':
        continue
      nm, kwargs = self._parse_param(k, v)
      p.add_argument(nm, **kwargs)
      n_args += 1

    delattr(self, '_parser_opts')
    delattr(self, '_arg_opts')
    self._parser = p
    self.n_args = n_args
    return p

  @property
  def __doc__(self):
    parser = self._parser if self._parser else self._make_parser()
    return parser.format_help()

  def __call__(self, self_, args):
    parser = self.parser if self._parser else self._make_parser()
    if self.n_args > 0:
      pp = parser.parse_args(args)
      return self.func(self_, **pp.__dict__)
    else:
      return self.func(self_)


def register_magic(
  name: [str, None] = None,
  parser_opts: dict = {},
  arg_opts: dict = {},
  is_method: bool = True,
  prefix: str = '%'
):
  """Function decorator that creates magics accessible via command line.

  Usage:

    @register_magic(name='magic_func',
      arg_opts={'arg1':{'help': 'help for arg1'}})
    def func(arg1, arg2: str, arg3: [None, str], arg4='test', arg5: float = 4.5, arg6: [str, bytes] = b'test_arg6'):
      ...

  Now you can call the function with a string a la:

    func('%magic_func 1 "arg2" "arg3" --arg4 "example test"')

  This is useful for emulating command line input.

  Note: Arguments in `argparse` objects can only take one type as an argument. If you annotate an argument in your signature with more than one type, then no type will be passed for that argument. In the example above the type on `arg5` will always be `float`. However, there is no type passed for `arg6`.

  Args:
      name (str, None, optional): Name of magic that will be used to call it from the command line. If no name is provided, then the name of the function is used.
      parser_opts (dict, optional): Additional commands to pass to the ArgumentParser object. See the argparse [docs](https://docs.python.org/3/library/argparse.html#argumentparser-objects) 
      arg_opts (dict, optional): Additional commands to pass when each argument of the function is added to the parser. Should be organized as a dict of dicts with top-level keys equal to an argument and values as dicts with valid `ArgumentParser.add_argument` options. See the [argparse docs](https://docs.python.org/3/library/argparse.html#the-add-argument-method) for the full set of options.
  """

  nm = ''

  def decorator(func: typing.Callable):
    nm = name if name else func.__name__.split('mgc_')[-1]
    return YapijMagicFunction(
      name=nm,
      func=func,
      parser_opts=parser_opts,
      arg_opts=arg_opts,
      is_method=is_method,
      prefix=prefix
    )

  decorator.__name__ = nm
  return decorator
