from .parser import parse_one
from .dialects import get_dialect, Snowflake
from .tokenizer import Tokenizer as _Tokenizer


def tokenize(sql: str, read=None):
    """Tokenize SQL using the specified dialect (default: ansi)."""
    dialect = get_dialect(read)
    return dialect.Tokenizer(sql).tokenize()


__all__ = [
    "parse_one",
    "tokenize",
    "get_dialect",
    "Snowflake",
]
