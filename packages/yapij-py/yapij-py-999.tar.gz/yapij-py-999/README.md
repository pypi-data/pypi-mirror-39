# `yapij-python`: Python-side of `yapij` package.

## Implementation Details

There are two key challenges that one faces when implementing an interpreter emulator:

1. Catching and processing program output.
1. Interrupting code before it is completed.

At the same time, we'd also like:

1. The ability to send other commands to the python process _while code is running._ For example, save a workspace while code is running.
1. Check on the health of the process with a heartbeat.

The main ingredients of the solution are:

1. Multi-threading for a main interface, the interpreter, and a heartbeat.
1. `asyncio` scheduling off the main loop.
1. Context managers that overwrite `sys.stdout` and `sys.stderr` with an emulator. _Appropriate placement of the context managers are key!_

### Misc. Details

#### Placement of context managers

A context manager that is called within a thread will "bubble up" to parent threads so long as it is running. See the [appendix example](#context-managers-in-a-thread). (However, there is no "bubbling down" from parent to child threads.)

This is problematic in our context because the threads will run as long as the context. (Therefore, `Thread.join` is not an option.)

Therefore, we place `catch_output` - the main context manager that formats `print` statements, exceptions, and `sys.stdout` in general - in the child thread `ExecSession`. This thread executes commands sent to the editor.

All such similar statements in the main thread are also handled by `catch_output` due to the "bubbling up" behavior.

### Rejected Alternatives

- Use standard `exec` and `runpy` to excute input:
  - Built-in module `code` provides `InteractiveInterpreter` and `InteractiveConsole` classes for doing just this.
  - Running code on instances of these objects still blocks. Therefore, does nothing for the `KeyboardInterrupt` problem.
  - Also do nothing for the last line print.

## Known Issues and Limitations

### Execution

#### Threading

- The session interpreter runs on its own thread. Therefore, certain applications may not run as expected.
- For example, the `signal` module cannot run on a non-main thread.
- Consider flipping around so that "main" thread is `ExecSession`.

#### `sys.stdout` and `sys.stderr`

- In order to communicate with the node process, `sys.stdout` and `sys.stderr` are overridden with an instance of a custom class `ZMQIOWrapper`.
- The custom class is built to emulate the classes underlying `sys.stdout`. In particular, it inherits class `io.TextIOWrapper`.
- However, full equivelance is not gauranteed at this time.
- Moreover, attempts to re-route `sys.stdout` from within the interpreter may not work as expected or may fail to revert as expected.

### Security

The point of this module is to permit _arbitrary code execution_. It is by no means secure.

#### Workspace Manager

- The workspace manager currently saves objects using the `dill` module, which is based on `pickle`
- We use `dill` because it allows us to preserve the state of a huge range of objects.
- The problem is that, if it is possible to pickle anything, then it will also be possible to pickle malicious code.
  - See the useful articles by [Nicolas Lara](https://lincolnloop.com/blog/playing-pickle-security/) and [Kevin London](https://www.kevinlondon.com/2015/08/15/dangerous-python-functions-pt2.html).
  - An example of a malicious `dill` exploit can be found in the [appendix](#a-dill-exploit)
- The current approach is to add a key to each file following the approach outlined [here](https://www.synopsys.com/blogs/software-security/python-pickling/).
  - This will raise a flag and fail to load if the generated key does not match the data.
  - **_It cannot protect in cases where someone malicious correctly decodes then re-encodes a file (or puts malicious code in the file to start)._**
  - Thus, this is best thought of as a way of being protected from code that might be naively injected into the pickled workspace when it is transferred between two known users (i.e. via a poorly-executed [man-in-the-middle attack](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).)
- Further refinements might included using `pickletools.dis` to inspect files for red flags. (See the [example](#a-dill-exploit) code for what that spits out.)
  - This will still never be completely secure.
- Jupyter Notebook stores keys in a separate `db`.
  - [Docs](https://jupyter-notebook.readthedocs.io/en/stable/security.html#the-details-of-trust)
  - [Some code references](https://github.com/jupyter/jupyter_core/blob/f1e18b8a52cd526c0cd1402b6041778dd60f20dc/jupyter_core/migrate.py#L16)
  - Where would it be stored on this module? How is db started?

#### A "Safe Mode"?

- It is really hard to do anything like a sandbox for python.
- In Python 2.3 [`rexec`](https://docs.python.org/2/library/restricted.html) was disabled due to "various known and not readily fixable security holes."
- Therefore, we take the stance that - instead of trying to offer security some of the time - we will always allow arbitrary execution in the hopes that this keeps users vigilant.

#### Security Best Practices

Best practices for yapij are identical to best practices for running any python code:

- Never load a workspace from someone that you do not know and trust.
- Never install a python package that you do not know or trust.

## Packaging

- Packaging is carried out with [PyPRI](https://www.python-private-package-index.com/).
- A new version is compiled by a job (using `.gitlab-ci.yaml`) every time that the a new commit is pushed with version (I think it depends on a tag being added.)
- Go to CLI to see the jobs.
- Use `pipreqs yapij` to make `requirements.txt`

### Dependencies

The main non-standard dependencies are:

- **[`pyzmq`/`zmq`](https://github.com/zeromq/pyzmq)**: "ØMQ is a lightweight and fast messaging implementation."
- **[`msgpack_python`/`msgpack`](https://github.com/msgpack/msgpack-python)**: "MessagePack is an efficient binary serialization format. It lets you exchange data among multiple languages like JSON. But it's faster and smaller."
- **[`dill`](https://pypi.org/project/dill/)**: "dill extends python’s pickle module for serializing and de-serializing python objects to the majority of the built-in python types."

We also provide custom serialization for `NumPy` arrays and `Pandas` dataframes. Thus, these become dependencies as well.

## About

### Contact

Michael Wooley

[michael.wooley@us.gt.com](mailto:michael.wooley@us.gt.com)

[michaelwooley.github.io](michaelwooley.github.io)

### License

UNLICENSED

(Sorry, not my choice.)

## Appendix

### A `dill` Exploit

Drawn from [Kevin London's _Dangerous Python Functions, Part 2_](https://www.kevinlondon.com/2015/08/15/dangerous-python-functions-pt2.html)

```python
import os
import dill
import pickletools

# Exploit that we want the target to unpickle
class Exploit(object):
    def __reduce__(self):
        # Note: this will only list files in your directory.
        # It is a proof of concept.
        return (os.system, ('dir',))


def serialize_exploit():
    shellcode = dill.dumps({'e': Exploit(), 's': dill.dumps})
    return shellcode


def insecure_deserialize(exploit_code):
    dill.loads(exploit_code)


if __name__ == '__main__':
    shellcode = serialize_exploit()
    print('~'*80,'IF I CAN SEE YOUR FILES I CAN USUALLY DELETE THEM AS WELL', '~'*80, sep='\n')
    insecure_deserialize(shellcode)

    print('~'*80,'WHAT IF WE MADE USE OF SHELL CODE TO LOOK FOR RED FLAGS LIKE "REDUCE"?', '~'*80, sep='\n')
    pickletools.dis(shellcode)
```

### Context managers in a thread

```python
import threading
import os
import sys
import contextlib
import copy

# Original
print_original = copy.copy(__builtins__.print)

def print_modified(*objects, sep=' ', end='\n', file=sys.stdout, flush=True):
  return print_original('[Context]', *objects, sep=sep, end=end, file=file, flush=flush)

@contextlib.contextmanager
def catch_output():
  try:
    __builtins__.print = print_modified
    yield
  finally:
    __builtins__.print = print_original

class WorkerThread(threading.Thread):

  def run(self):
    with catch_output(False):
      time.sleep(3)
      print('Inside Context')
    time.sleep(3)
    print('Outside Context')

w = WorkerThread()
w.start()
print('Yep')
```

Will return something like:

```
[Context] Yep
[Context] Inside Context
Outside Context
```
