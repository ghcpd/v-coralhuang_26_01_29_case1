from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Iterable, List, Tuple


class TokenType(Enum):
    # Core lexical tokens
    EOF = auto()
    COMMENT = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    COMMA = auto()
    STAR = auto()
    LPAREN = auto()
    RPAREN = auto()
    DOT = auto()
    COLON = auto()
    SLASH = auto()
    DASH = auto()
    PLUS = auto()
    MUL = auto()
    EQ = auto()

    # Keywords
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    AS = auto()
    TABLE = auto()
    RLIKE = auto()
    LIKE_ANY = auto()
    ILIKE_ANY = auto()
    EXCEPT = auto()
    MATCH_RECOGNIZE = auto()
    COMMAND = auto()
    REPLACE = auto()
    TIMESTAMPLTZ = auto()
    TIMESTAMP = auto()
    TIMESTAMPTZ = auto()
    TABLE_SAMPLE = auto()
    VARCHAR = auto()
    TIME = auto()
    PARAMETER = auto()

    # Fallback for anything unclassified
    UNKNOWN = auto()


@dataclass
class Token:
    token_type: TokenType
    text: str

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"Token({self.token_type.name}, {self.text!r})"


# Default keyword mapping (upper-cased input is looked up)
DEFAULT_KEYWORDS: Dict[str, TokenType] = {
    "SELECT": TokenType.SELECT,
    "FROM": TokenType.FROM,
    "WHERE": TokenType.WHERE,
    "AS": TokenType.AS,
    "TABLE": TokenType.TABLE,
    "RLIKE": TokenType.RLIKE,
    "LIKE ANY": TokenType.LIKE_ANY,
    "ILIKE ANY": TokenType.ILIKE_ANY,
    "EXCEPT": TokenType.EXCEPT,
    "MATCH_RECOGNIZE": TokenType.MATCH_RECOGNIZE,
    "PUT": TokenType.COMMAND,
    "RENAME": TokenType.REPLACE,
    "TIMESTAMP_LTZ": TokenType.TIMESTAMPLTZ,
    "TIMESTAMP_NTZ": TokenType.TIMESTAMP,
    "TIMESTAMP_TZ": TokenType.TIMESTAMPTZ,
    "TIMESTAMPNTZ": TokenType.TIMESTAMP,
    "SAMPLE": TokenType.TABLE_SAMPLE,
    "VARCHAR": TokenType.VARCHAR,
    "TIME": TokenType.TIME,
}

# Default single-character tokens
DEFAULT_SINGLE_TOKENS: Dict[str, TokenType] = {
    ",": TokenType.COMMA,
    "*": TokenType.STAR,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    ".": TokenType.DOT,
    ":": TokenType.COLON,
    "/": TokenType.SLASH,
    "-": TokenType.DASH,
    "+": TokenType.PLUS,
    "=": TokenType.EQ,
}


# Comment configurations
# Each dialect can override these. Base tokenizer will always recognize template comments '{# ... #}'.
DEFAULT_LINE_COMMENT_PREFIXES: Tuple[str, ...] = ("--",)
DEFAULT_BLOCK_COMMENT_DELIMS: Tuple[Tuple[str, str], ...] = (("/*", "*/"),)
DEFAULT_TEMPLATE_COMMENT_DELIM: Tuple[str, str] = ("{#", "#}")


__all__ = ["TokenType", "Token", "DEFAULT_KEYWORDS", "DEFAULT_SINGLE_TOKENS", "DEFAULT_LINE_COMMENT_PREFIXES", "DEFAULT_BLOCK_COMMENT_DELIMS", "DEFAULT_TEMPLATE_COMMENT_DELIM"]
