import io
import sys
import zmq
from msgpack import packb

try:
  from . import packers
except (ModuleNotFoundError, ImportError):
  import packers


class ZMQIOWrapper(io.TextIOWrapper):
  """Extend IO for ZMQ

  [Reference to TextIOWrapper.write](https://github.com/python/cpython/blob/master/Lib/_pyio.py#L2135) Note that this is for 

  Attributes:
      pub (TYPE): Description
      topic (TYPE): Description
  """

  def __init__(
    self,
    buf: io.BufferedWriter,
    pub: zmq.Socket,
    topic: bytes,
    encoding: str = 'utf-8'
  ):
    super().__init__(
      buffer=buf,
      line_buffering=True,
      write_through=True,
      errors='replace'
    )

    self.newline = (None, "", "\n", "\r", "\r\n")

    self._pub = pub
    self._topic = topic

  def write(self, s: [bytes, str]) -> int:

    if isinstance(s, str):
      if s not in self.newline:
        le, pe = packers.pack_implicit(s)
        s = packb(pe(le))
      else:
        s = packb(s)

    self.pub.send_multipart([self.topic, s])

    return len(s)

  @property
  def closed(self):
    return self.pub.closed * self.buffer.closed

  @property
  def pub(self):
    return self._pub

  @property
  def topic(self):
    return self._topic