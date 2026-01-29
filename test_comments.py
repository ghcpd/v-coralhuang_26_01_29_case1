"""unittest discovery entrypoint.

The main test implementations live in `issue_test.py` per the exercise prompt.
This file exists so `python -m unittest -v` (default pattern `test*.py`) finds them.
"""

from issue_test import *  # noqa: F401,F403
