import time
import threading
import zmq
import sys
import os
import traceback
import asyncio

try:
  from .workers import Heartbeat, ExecSession
  from .manager import ZmqManager
  from .threading2 import Thread2
  from .exceptions import YapijError
  from .config import encoding
except (ModuleNotFoundError, ImportError):
  from workers import Heartbeat, ExecSession
  from manager import ZmqManager
  from threading2 import Thread2
  from exceptions import YapijError
  from config import encoding


class Client(Thread2):
  SUB_GLOBAL = b'PY_EXEC'
  SUB_QUIT_GLOBAL = b'PY_QUIT'
  PUB_STATUS_GLOBAL = b'PY_STATUS'
  PUB_TOPIC = b'PY_OUT'

  def __init__(
    self, ports: dict, cmd_opts: dict, heartbeat_interval: int, key: str
  ):
    super().__init__()

    self.ports = ports

    self.cmd_opts = cmd_opts
    self.heartbeat_interval = heartbeat_interval
    self.key = bytes(key, encoding)

    self.SUB = b'_'.join([self.SUB_GLOBAL, self.key])
    self.SUB_QUIT = b'_'.join([self.SUB_QUIT_GLOBAL, self.key])
    self.PUB_TOPIC = b'_'.join([self.PUB_TOPIC, self.key])
    self.PUB_STATUS = b'_'.join([self.PUB_STATUS_GLOBAL, self.key])

    self.setDaemon(True)

  def run(self):
    self.context = zmq.Context()

    sub = self.context.socket(zmq.SUB)
    sub.connect(self.ports['frontend'])
    sub.setsockopt(zmq.SUBSCRIBE, self.SUB)
    sub.setsockopt(zmq.SUBSCRIBE, self.SUB_QUIT)
    sub.setsockopt(zmq.SUBSCRIBE, self.SUB_QUIT_GLOBAL)

    pub = self.context.socket(zmq.PUB)
    pub.connect(self.ports['backend'])

    self.sub = sub
    self.pub = pub

    self._init_children()
    self.mgmt = ZmqManager(
      self.tasks['exec_session'], self.exec_loop, self.pub, self.PUB_TOPIC,
      self.PUB_STATUS, **self.cmd_opts
    )
    self.mgmt.do_init()

    try:
      while True:
        topic, uid, msg = self.sub.recv_multipart()
        if topic == self.SUB:
          # Route it through MGMT
          self.mgmt(uid, msg)
        elif topic == self.SUB_QUIT or topic == self.SUB_QUIT_GLOBAL:
          self.stop()
          sys._exit(1)
        else:
          raise YapijError(
            'TOPIC `{}` cannot be handled by Session thread. Communication from connection: `{}`'
            .format(topic, self.ports['frontend'])
          )
    except Exception as e:
      raise e
      exc_type, exc_value, exc_tb = sys.exc_info()
      tb = traceback.format_exception(exc_type, exc_value, exc_tb)

      print('YAPIJ PYTHON FATAL ERROR: ', file=sys.stderr)
      print('\n'.join(tb), file=sys.stderr, flush=True)
    finally:
      self.stop()

    return None

  def _init_children(self):
    self.tasks = {}

    # Heartbeat
    hb = Heartbeat(self.context, self.ports, self.heartbeat_interval)
    hb.start()
    self.tasks['heartbeat'] = hb

    # Main Execution Thread
    self.exec_loop = asyncio.new_event_loop()
    ex = ExecSession(self.context, self.ports, self.key, self.exec_loop)
    ex.start()
    self.tasks['exec_session'] = ex

  def stop(self):
    self.mgmt.session.interrupt()
    self.tasks[1].call_soon_threadsafe(self.event_loop.close)
    for task in self.tasks.values():
      task.stop()
    self.sub.close()
    self.pub.close()
    self.context.term()
    self.terminate()
