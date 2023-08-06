import argparse
from getpass import getuser


def parse() -> argparse.Namespace:
  parser = argparse.ArgumentParser(
    description='YAPIJ: Interactive Python from Node [Python side]'
  )

  parser.add_argument(
    '--backend',
    '-bp',
    type=str,
    help='Ports on which to connect for backend. (Required)'
  )

  parser.add_argument(
    '--frontend',
    '-fp',
    type=str,
    help='Ports on which to connect for frontend. (Required)'
  )

  parser.add_argument(
    '--heartbeat_port',
    '-hp',
    type=str,
    help='Ports on which to connect for heartbeat (Required)'
  )

  parser.add_argument(
    '--heartbeat_interval',
    '-heart',
    type=int,
    default=120,
    help='Seconds to wait between sending heartbeats. (Required, default=120)'
  )

  parser.add_argument(
    '-f',
    '--init_filename',
    metavar='INIT_FILENAME',
    type=str,
    default=None,
    help='Filename of environment at initialization. If filename exists, will load the file. If it does not, will initialize a new environment with that filename.  (default: None)'
  )

  parser.add_argument(
    '--user',
    '-u',
    metavar='USER',
    type=str,
    default=getuser(),
    help='Name of user. (Default: Computer profile login name)'
  )

  parser.add_argument(
    '-s',
    '--startup_script',
    metavar='STARTUP_SCRIPT',
    type=str,
    default='',
    help='Code to be run once the environment is created. (default: \'\')'
  )

  parser.add_argument(
    '-k',
    '--key',
    metavar='KEY',
    type=str,
    help='Key that uniquelly identifies/links this key with its parent node process.'
  )

  parser.add_argument(
    '-cd',
    '--cd',
    metavar='CD',
    type=str,
    default=None,
    help='Key that uniquelly identifies/links this key with its parent node process.'
  )

  # PARSE ARGS IN HERE!
  pa = parser.parse_args()

  return {
    'ports':
      {
        'backend': pa.backend,
        'frontend': pa.frontend,
        'heartbeat': pa.heartbeat_port
      },
    'cmd_opts':
      {
        'init_filename': pa.init_filename,
        'user': pa.user,
        'startup_script': pa.startup_script,
        'cd': pa.cd,
      },
    'heartbeat_interval': pa.heartbeat_interval,
    'key': pa.key,
  }
