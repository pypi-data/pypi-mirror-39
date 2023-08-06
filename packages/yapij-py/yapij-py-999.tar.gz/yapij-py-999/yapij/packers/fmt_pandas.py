def fmt_frame(d):
  """Format the dataframe
  """
  return {
    'd': [_fmt_values(v) for _, v in d.iteritems()],  # data
    'i':
      {
        'v': fmt_index(d.index),
        't': str(type(d.index)).split('\'')[1].split('.')[-1]
      },  # index
    'c':
      {
        'v': fmt_index(d.columns),
        't': [v.dtype.kind for _, v in d.iteritems()]
      },  # columns
    's': list(d.shape),  # shape
  }


def fmt_series(d):

  return {
    'd': _fmt_values(d),  # data
    'i':
      {
        'v': fmt_index(d.index),
        't': str(type(d.index)).split('\'')[1].split('.')[-1]
      },  # index
    'c': d.name.__str__(),  # name
    's': list(d.shape),  # shape
  }


def _fmt_values(d):

  ds = str(d.dtype)

  if ds.startswith('float') or ds.startswith('int'):
    return d.values.tolist()
  else:
    return d.astype(str).values.tolist()


def fmt_index(d):
  return d.astype(str).values.tolist()


def fmt_period(d):
  return {'d': d.__str__(), 'f': d.freqstr}


def fmt_timestamp(d):
  return d.__str__()