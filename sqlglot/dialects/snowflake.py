from __future__ import annotations

from ..tokenizer import Tokenizer
from ..parser import Parser
from .dialect import Dialect


class SnowflakeTokenizer(Tokenizer):
    # Include // as a single-line comment along with defaults
    COMMENT_SPEC = [("//", "\n"), ("--", "\n"), ("/*", "*/")]


class Snowflake(Dialect):
    Tokenizer = SnowflakeTokenizer
    Parser = Parser


__all__ = ["Snowflake", "SnowflakeTokenizer"]
