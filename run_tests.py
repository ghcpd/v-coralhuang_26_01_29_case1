"""
One-command test runner for this repository.
Usage:
    python run_tests.py
"""

import subprocess
import sys


def main() -> int:
    cmd = [sys.executable, "-m", "pytest", "-q"]
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
