from __future__ import annotations

import os
import sys
import unittest


def main() -> int:
    # Ensure discovery runs from the repo root even if invoked elsewhere.
    repo_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_root)

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=repo_root, pattern="test*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
