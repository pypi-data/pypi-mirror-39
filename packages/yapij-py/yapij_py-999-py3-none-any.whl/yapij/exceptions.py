"""https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
"""


class WorkerClose(Exception):
  """An "error" that will cause the processes to shut down.

  Attributes:
      errors (TYPE): Description
  """

  def __init__(self, message, errors):
    """Summary

    Args:
        message (TYPE): Description
        errors (TYPE): Description
    """
    # Call the base class constructor with the parameters it needs
    super().__init__(message)

    self.errors = errors


class InterruptExecution(InterruptedError):
  """An "error" that will cause execution to pause
  """


class YapijError(RuntimeError):
  """General error for cases relevant to yapij.
  """