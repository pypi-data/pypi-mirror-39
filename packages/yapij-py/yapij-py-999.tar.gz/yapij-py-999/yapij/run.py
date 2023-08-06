import os

try:
  from .parse import parse
  from .client import Client
except (ModuleNotFoundError, ImportError):
  from parse import parse
  from client import Client


def run():
  args = parse()
  pt = Client(
    ports=args['ports'],
    cmd_opts=args['cmd_opts'],
    heartbeat_interval=args['heartbeat_interval'],
    key=args['key']
  )
  pt.start()
  pt.join()


if __name__ == '__main__':
  run()