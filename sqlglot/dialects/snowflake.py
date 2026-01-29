from __future__ import annotations

from typing import Tuple

from ..parser import Parser as BaseParser
from ..tokenizer import Tokenizer as BaseTokenizer
from ..tokens import TokenType, DEFAULT_KEYWORDS, DEFAULT_SINGLE_TOKENS
from .dialect import Dialect


class Snowflake(Dialect):
    """
    Minimal Snowflake dialect implementation focused on comment handling (issue #1763).

    Snowflake supports three comment styles:
    - `--` single-line comments (ANSI-style)
    - `//` single-line comments (C++-style)
    - `/* ... */` block comments

    Additionally, template comments `{# ... #}` are always recognized by the base tokenizer
    across all dialects.
    """

    class Tokenizer(BaseTokenizer):
        # Snowflake allows $$-quoted strings and supports C++ style // comments
        QUOTES = ["'", "$$"]
        STRING_ESCAPES = ["\\", "'"]

        KEYWORDS = {
            **DEFAULT_KEYWORDS,
            "CHAR VARYING": TokenType.VARCHAR,
            "CHARACTER VARYING": TokenType.VARCHAR,
            "EXCLUDE": TokenType.EXCEPT,
            "ILIKE ANY": TokenType.ILIKE_ANY,
            "LIKE ANY": TokenType.LIKE_ANY,
            "MATCH_RECOGNIZE": TokenType.MATCH_RECOGNIZE,
            "MINUS": TokenType.EXCEPT,
            "NCHAR VARYING": TokenType.VARCHAR,
            "PUT": TokenType.COMMAND,
            "RENAME": TokenType.REPLACE,
            "TIMESTAMP_LTZ": TokenType.TIMESTAMPLTZ,
            "TIMESTAMP_NTZ": TokenType.TIMESTAMP,
            "TIMESTAMP_TZ": TokenType.TIMESTAMPTZ,
            "TIMESTAMPNTZ": TokenType.TIMESTAMP,
            "SAMPLE": TokenType.TABLE_SAMPLE,
        }

        SINGLE_TOKENS = {
            **DEFAULT_SINGLE_TOKENS,
            "$": TokenType.PARAMETER,
        }

        VAR_SINGLE_TOKENS: Tuple[str, ...] = ("$",)

        # ✅ Critical fix: include C++-style `//` single-line comments
        LINE_COMMENT_PREFIXES: Tuple[str, ...] = ("--", "//")
        BLOCK_COMMENT_DELIMS: Tuple[Tuple[str, str], ...] = (("/*", "*/"),)

    class Parser(BaseParser):
        # In a full implementation Snowflake would tweak many parser behaviors.
        # For this minimal reproduction, the base Parser already ignores comment tokens.
        IDENTIFY_PIVOT_STRINGS = True


__all__ = ["Snowflake"]
