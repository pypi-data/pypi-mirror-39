"""Defines msgpack packing protocols for different types of common python objects.

The most important attribute of this file is the definition of extension hooks for msgpack.

This file should only contain minimal handling for packing specific types of files. Otherwise, the inputs should be packaged in another function (e.g. in "printing") and sent here.

Attributes:
    PACK_DICT (TYPE): Description
"""
import types
from datetime import datetime

try:
  from .packers import *
except (ModuleNotFoundError, ImportError):
  import packers

__all__ = [
  'pack_explicit', 'pack_implicit', 'pack_generic', 'pack_exception',
  'pack_warning', 'pack_docstring'
]


def pack_dict_nested(uid, d):
  return pack_dict(
    uid, {k: pack_explicit(v)(uid, v)
          for k, v in d.items()}
  )


def pack_list_nested(uid, d):
  return pack_list(uid, [pack_explicit(v)(uid, v) for v in d])


def pack_tuple_nested(uid, d):
  return pack_tuple(uid, tuple(pack_explicit(v)(uid, v) for v in d))


def pack_set_nested(uid, d):
  return pack_set(uid, {pack_explicit(v)(uid, v) for v in d})


def pack_frozenset_nested(uid, d):
  return pack_frozenset(
    uid, frozenset({pack_explicit(v)(uid, v)
                    for v in d})
  )


PACK_DICT = {
  Exception: pack_exception,
  Warning: pack_warning,
  int: pack_int,
  float: pack_float,
  complex: pack_complex,
  # Iter
  list: pack_list_nested,
  tuple: pack_tuple_nested,
  range: pack_range,
  str: pack_str,
  bytes: pack_bytes,
  bytearray: pack_bytearray,
  memoryview: pack_memoryview,
  set: pack_set,
  frozenset: pack_frozenset_nested,
  dict: pack_dict_nested,
  # ContextManager
  types.ModuleType: pack_module,
  types.FunctionType: pack_function,
  types.MethodType: pack_method,
  types.CodeType: pack_code,
  type: pack_type,
  # None
  # ellipsis
  # NotImplemented
  bool: pack_bool,
  datetime: pack_datetime
}

PACK_DICT_NON_BUILTIN = {
  "<class 'pandas.core.frame.DataFrame'>": pack_dataframe,
  "<class 'pandas.core.series.Series'>": pack_series,
  "<class 'numpy.ndarray'>": pack_array,
  "<class 'matplotlib.figure.Figure'>": pack_figure
}


def pack_explicit(d):

  pt = PACK_DICT.get(type(d), None)
  if pt:
    return pt

  pt = PACK_DICT_NON_BUILTIN.get(repr(type(d)), None)

  if pt:
    return pt
  elif hasattr(d, '__iter__'):
    return pack_iter
  elif hasattr(d, '__enter__') and hasattr(d, '__exit__'):
    return pack_contextManager
  elif d is None:
    return pack_null
  elif d is Ellipsis:
    return pack_ellipsis
  elif d is NotImplemented:
    return pack_NotImplemented
  else:
    return pack_unknown


# def get_pack(uid):
#   def inner(obj):
#     return pack_explicit(obj)(uid, obj)

#   return inner

# class Packer(object):
#   def __init__(self, uid=None):
#     self.uid = uid

#   def pack(self, obj):
#     p = self.pack_explicit(obj)
#     return p(self.uid, obj)

#   def pack_explicit(self, d):

#     pt = PACK_DICT.get(type(d), None)
#     if pt:
#       return pt

#     pt = PACK_DICT_NON_BUILTIN.get(repr(type(d)), None)

#     if pt:
#       return pt
#     elif hasattr(d, '__iter__'):
#       return pack_iter
#     elif hasattr(d, '__enter__') and hasattr(d, '__exit__'):
#       return pack_contextManager
#     elif d is None:
#       return pack_null
#     elif d is Ellipsis:
#       return pack_ellipsis
#     elif d is NotImplemented:
#       return pack_NotImplemented
#     else:
#       return pack_unknown
