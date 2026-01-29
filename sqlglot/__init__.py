"""
Minimal local sqlglot implementation for comment parsing tests.
This is intentionally limited to the features exercised by the repository tests.
"""
from __future__ import annotations

from typing import Any, Optional, Union

from . import exp
from .parser import parse_one
from .dialects import dialects  # type: ignore

__all__ = ["parse_one", "exp", "dialects"]
