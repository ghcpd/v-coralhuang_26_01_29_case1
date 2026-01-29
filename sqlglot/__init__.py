from __future__ import annotations

from typing import Optional

from . import expressions as exp
from .parser import Parser
from .tokenizer import Tokenizer
from .dialects import Snowflake

# Mapping of dialect name to class
_DIALECTS = {
    "snowflake": Snowflake,
    "snow": Snowflake,
    "default": Snowflake,
    "ansi": Snowflake,  # keep single dialect for minimal demo
}


def dialects():
    """Return available dialect classes."""
    return _DIALECTS


def parse_one(sql: str, read: Optional[str] = None):
    """Parse a single SQL statement and return an Expression.

    Comments are ignored during parsing. Dialect selection controls comment tokenization rules
    (e.g., Snowflake supports `//` line comments).
    """

    dialect_key = (read or "default").lower() if isinstance(read, str) else "default"
    dialect_cls = _DIALECTS.get(dialect_key)
    if dialect_cls is None:
        raise ValueError(f"Unknown dialect: {read}")

    expressions = dialect_cls.parse(sql)
    return expressions[0] if expressions else None


__all__ = ["parse_one", "exp", "Parser", "Tokenizer", "Snowflake", "dialects"]
