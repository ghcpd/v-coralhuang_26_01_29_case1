#!/usr/bin/env python
"""
One-command test runner for this repository.
Usage:
    python run_tests.py          # runs full test suite
    python run_tests.py -q       # optional: quiet mode
Prerequisites: `pytest` installed (pip install pytest)
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parent
    python = sys.executable or "python"

    # Check pytest availability via import to avoid PATH issues on Windows
    try:
        import importlib.util

        if importlib.util.find_spec("pytest") is None:  # type: ignore[attr-defined]
            raise ImportError
    except ImportError:
        print("pytest not found. Install it with: python -m pip install pytest", file=sys.stderr)
        return 1

    cmd = [python, "-m", "pytest", *argv]
    return subprocess.call(cmd, cwd=root)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv[1:]))
