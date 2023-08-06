import msgpack
from . import fmt_pandas
from . import fmt_special

# HACK
try:
  from .config import use_bin_type
except:
  use_bin_type = False
"""
Builtin Python Types.

Drawn from: https://docs.python.org/3/library/stdtypes.html#bytearray-objects
"""


def pack_exception(uid, d):
  return msgpack.ExtType(
    1,
    msgpack.packb(
      [uid, fmt_special.fmt_exception(d)], use_bin_type=use_bin_type
    )
  )


def pack_warning(uid, d):
  return msgpack.ExtType(
    2,
    msgpack.packb(
      [uid, fmt_special.fmt_warning(d)], use_bin_type=use_bin_type
    )
  )


def pack_int(uid, d):
  return msgpack.ExtType(
    3, msgpack.packb([uid, d], use_bin_type=use_bin_type)
  )


def pack_float(uid, d):
  return msgpack.ExtType(
    4, msgpack.packb([uid, d], use_bin_type=use_bin_type)
  )


def pack_complex(uid, d):
  return msgpack.ExtType(
    5,
    msgpack.packb(
      [uid, {
        'r': d.real,
        'i': d.imag
      }], use_bin_type=use_bin_type
    )
  )


def pack_iter(uid, d):
  return msgpack.ExtType(
    6, msgpack.packb([uid, str(d)], use_bin_type=use_bin_type)
  )


def pack_list(uid, d):
  return msgpack.ExtType(
    7, msgpack.packb([uid, d], use_bin_type=use_bin_type)
  )


def pack_tuple(uid, d):
  return msgpack.ExtType(
    8, msgpack.packb([uid, d], use_bin_type=use_bin_type)
  )


def pack_range(uid, d):
  return msgpack.ExtType(
    9, msgpack.packb([uid, str(d)], use_bin_type=use_bin_type)
  )


def pack_str(uid, d):
  return msgpack.ExtType(
    10, msgpack.packb([uid, d], use_bin_type=use_bin_type)
  )


def pack_bytes(uid, d):
  return msgpack.ExtType(
    11, msgpack.packb([uid, str(d)], use_bin_type=use_bin_type)
  )


def pack_bytearray(uid, d):
  return msgpack.ExtType(
    12, msgpack.packb([uid, str(d)], use_bin_type=use_bin_type)
  )


def pack_memoryview(uid, d):
  return msgpack.ExtType(
    13,
    msgpack.packb(
      [uid, {
        'l': d.tolist(),
        's': d.shape,
        'b': d.nbytes
      }],
      use_bin_type=use_bin_type
    )
  )


def pack_set(uid, d):
  return msgpack.ExtType(
    14, msgpack.packb([uid, list(d)], use_bin_type=use_bin_type)
  )


def pack_frozenset(uid, d):
  return msgpack.ExtType(
    15, msgpack.packb([uid, list(d)], use_bin_type=use_bin_type)
  )


def pack_dict(uid, d):
  return msgpack.ExtType(
    16, msgpack.packb([uid, d], use_bin_type=use_bin_type)
  )


def pack_contextManager(uid, d):
  return msgpack.ExtType(
    17, msgpack.packb([uid, str(d)], use_bin_type=use_bin_type)
  )


def pack_module(uid, d):
  return msgpack.ExtType(
    18,
    msgpack.packb(
      [
        uid,
        {
          'n': getattr(d, '__name__', 'unknown'),
          'dir': dir(d),
          'doc': getattr(d, '__doc__', '')
        }
      ],
      use_bin_type=use_bin_type
    )
  )


def pack_function(uid, d):
  return msgpack.ExtType(
    19,
    msgpack.packb(
      [uid, {
        'n': getattr(d, '__name__', '{{UNKNOWN}}'),
        's': str(d)
      }],
      use_bin_type=use_bin_type
    )
  )


def pack_method(uid, d):
  n = getattr(d, '__func__', '{{UNKNOWN}}')
  if n != '{{UNKNOWN}}':
    n = getattr(n, '__name__', '{{UNKNOWN}}')

  return msgpack.ExtType(
    20,
    msgpack.packb([uid, {
      'n': n,
      's': str(d)
    }], use_bin_type=use_bin_type)
  )


def pack_code(uid, d):
  return msgpack.ExtType(
    21, msgpack.packb([uid, str(d)], use_bin_type=use_bin_type)
  )


def pack_type(uid, d):
  return msgpack.ExtType(
    22,
    msgpack.packb([uid, str(d).split('\'')[1]], use_bin_type=use_bin_type)
  )


def pack_null(uid, d):
  return msgpack.ExtType(
    23, msgpack.packb([uid, None], use_bin_type=use_bin_type)
  )


def pack_ellipsis(uid, d):
  return msgpack.ExtType(
    24, msgpack.packb([uid, '...'], use_bin_type=use_bin_type)
  )


def pack_NotImplemented(uid, d):
  return msgpack.ExtType(
    25, msgpack.packb([uid, 'NotImplemented'], use_bin_type=use_bin_type)
  )


def pack_bool(uid, d):
  return msgpack.ExtType(
    26, msgpack.packb([uid, int(d)], use_bin_type=use_bin_type)
  )


def pack_datetime(uid, d):
  return msgpack.ExtType(
    27,
    msgpack.packb([uid, str(d.astimezone())], use_bin_type=use_bin_type)
  )


"""
  NUMPY+PANDAS+MATPLOTLIB: 90-100

  Other types to be added:

  PANDAS:
    Panel
    Index
    GroupBy

  NumPy:
    matrix
    dtypes

  COMBINED:
    dtypes (np.float64, Timestamp, Period, etc.)

  PLOTTING:
    figure
"""

# def pack_dtypes(uid,d):
#   return msgpack.ExtType(90, ...)


def pack_array(uid, d):
  return msgpack.ExtType(
    91,
    msgpack.packb(
      [uid, {
        'b': d.tolist(),
        's': d.shape,
        't': d.dtype.__str__()
      }],
      use_bin_type=use_bin_type
    )
  )


# def pack_matrix(uid, d):
#   return msgpack.ExtType(92, ...)

# def pack_index(uid, d):
#   return msgpack.ExtType(
#     93, ...
#   )


def pack_series(uid, d):
  return msgpack.ExtType(
    94,
    msgpack.packb(
      [uid, fmt_pandas.fmt_series(d)], use_bin_type=use_bin_type
    )
  )


def pack_dataframe(uid, d):
  return msgpack.ExtType(
    95,
    msgpack.packb(
      [uid, fmt_pandas.fmt_frame(d)], use_bin_type=use_bin_type
    )
  )


# def pack_panel(uid, d):
#   return msgpack.ExtType(
#     96, ...
#   )

# def pack_groupby(uid, d):
#   return msgpack.ExtType(
#     97, ...
#   )


def pack_figure(uid, d):
  return msgpack.ExtType(
    99,
    msgpack.packb(
      [uid, fmt_special.fmt_figure(d)], use_bin_type=use_bin_type
    )
  )


"""
TYPES PARTICULAR TO YAPIJ
"""


def pack_end(uid, d):
  return msgpack.ExtType(
    124, msgpack.packb([uid, d], use_bin_type=use_bin_type)
  )


def pack_sep(uid, d):
  return msgpack.ExtType(
    125, msgpack.packb([uid, d], use_bin_type=use_bin_type)
  )


def pack_docstring(uid, d):
  # 106
  return msgpack.ExtType(
    126,
    msgpack.packb(
      [uid, fmt_special.fmt_docstring(d)], use_bin_type=use_bin_type
    )
  )


def pack_unknown(uid, d):
  return msgpack.ExtType(
    127,
    msgpack.packb(
      [uid, {
        'str': str(d),
        'type': str(type(d)).split('\'')[1]
      }],
      use_bin_type=use_bin_type
    )
  )