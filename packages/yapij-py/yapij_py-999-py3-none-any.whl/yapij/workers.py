import os
import time
import zmq
import typing
import re
import sys
import traceback
import asyncio
import threading

try:
  from .threading2 import Thread2
  from .context import create_catch_output
  from .config import encoding
except (ModuleNotFoundError, ImportError):
  from threading2 import Thread2
  from context import create_catch_output
  from config import encoding

__all__ = ['Heartbeat', 'ExecSession']


class Heartbeat(Thread2):
  def __init__(
    self, context: zmq.Context, ports: dict, heartbeat_interval: int
  ):
    super().__init__()

    self.context = context
    self.ports = ports
    self.heartbeat_interval = heartbeat_interval

    self._stop_signal = threading.Event()
    self.sockets = []
    self.setDaemon(True)

    self.strikes = 0
    self.max_strikes = -1
    self.total_time = 0

  def _check_poll(self, timeout: float):
    socks = dict(self.poller.poll(1000 * timeout))
    if socks.get(self.rep, None) == zmq.POLLIN:
      request = self.rep.recv()
      self.strikes = 0
      self.total_time = 0
      self.rep.send(request)
    else:
      self.strikes += 1
      self.total_time += timeout
      if self.strikes > self.max_strikes:
        msg = 'YAPIJ PYTHON FATAL HEARTBEAT ERROR: No new beats in last {:4.1f} seconds. Shutting down.'.format(
          self.total_time
        )
        print(msg, file=sys.stderr)
        self.rep.close()
        self.poller.close()
        self._stop_signal.set()
        # raise RuntimeError
        os._exit(0)

    return None

  def run(self):

    rep = self.context.socket(zmq.REP)
    rep.connect(self.ports['heartbeat'])

    poller = zmq.Poller()
    poller.register(rep, zmq.POLLIN)

    self.rep = rep
    self.poller = poller

    # Initial check for signal (Try to reply quickly on startup)
    self.max_strikes = 99
    for _ in range(100):
      self._check_poll(0.1)

    self.max_strikes = 2
    while not self._stop_signal.is_set() and not self.rep.closed:
      self._check_poll(self.heartbeat_interval)

  def stop(self):
    self.rep.close()
    self.poller.close()
    self._stop_signal.set()
    self.terminate()


class ExecSession(Thread2):
  PUB_GLOBAL = b'PY_OUT'

  def __init__(
    self, context: zmq.Context, ports: dict, key: bytes,
    loop: asyncio.AbstractEventLoop
  ):

    super().__init__()

    self.context = context
    self.ports = ports
    self.loop = loop
    self._stop_signal = threading.Event()
    self.key = key

    self.PUB = b'_'.join([self.PUB_GLOBAL, self.key])

    self.setDaemon(True)

  def run(self):

    self.pub = self.context.socket(zmq.PUB)
    self.pub.connect(self.ports['backend'])

    _, catch_output = create_catch_output(self.pub, self.PUB)

    try:
      asyncio.set_event_loop(self.loop)
      with catch_output():
        self.loop.run_forever()
    except Exception as e:
      exc_type, exc_value, exc_tb = sys.exc_info()
      tb = traceback.format_exception(exc_type, exc_value, exc_tb)

      print('YAPIJ PYTHON FATAL SESSION ERROR: ', file=sys.stderr)
      print('\n'.join(tb), file=sys.stderr, flush=True)
    finally:
      self.stop()

  def stop(self):
    self.pub.close()
    self._stop_signal.set()
    self.terminate()
