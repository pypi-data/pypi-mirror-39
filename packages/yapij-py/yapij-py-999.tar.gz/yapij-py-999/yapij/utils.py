import socket


def check_open_port(port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.settimeout(5)
    s.bind(('127.0.0.1', int(port)))
    s.close()
    return True
  except OSError:
    return False


def get_open_ports(rng: list = [3000, 9000], tries: int = 400, n: int = 1):
  def inner():
    found, n = False, 0
    while not found and n < tries:
      port = random.choice(range(*rng))
      if check_open_port(port):
        found = True
        return port
      else:
        tries += 1

    raise OSError('Could not find an open port!')

  if n == 1:
    return inner()
  else:
    return [inner() for ii in range(n)]
