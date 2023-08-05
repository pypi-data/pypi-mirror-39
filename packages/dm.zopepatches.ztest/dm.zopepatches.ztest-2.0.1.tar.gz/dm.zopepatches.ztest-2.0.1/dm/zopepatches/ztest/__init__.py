"""'ztest' console script.

See 'README.txt' for an introduction.
Use 'ztest -h' to view the options.
"""
# work around a strange (not yet understood) Python 2.6.2 bug
import AccessControl

# werk around "https://bugs.python.org/issue35283"
from threading import _DummyThread
_DummyThread.isAlive = _DummyThread.is_alive

from .test import main
