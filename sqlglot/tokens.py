from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple


class TokenType(enum.Enum):
    # Core tokens
    SELECT = "SELECT"
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    STAR = "*"
    COMMA = ","
    LPAREN = "("
    RPAREN = ")"
    DOT = "."
    PLUS = "+"
    MINUS = "-"
    DIV = "/"
    FLOORDIV = "//"
    COLON = ":"
    EOF = "EOF"
    COMMENT = "COMMENT"

    # Dialect-specific placeholders (stubs for compatibility)
    RLIKE = "RLIKE"
    TABLE = "TABLE"
    TIME = "TIME"
    ILIKE_ANY = "ILIKE_ANY"
    LIKE_ANY = "LIKE_ANY"
    MATCH_RECOGNIZE = "MATCH_RECOGNIZE"
    EXCEPT = "EXCEPT"
    VARCHAR = "VARCHAR"
    COMMAND = "COMMAND"
    REPLACE = "REPLACE"
    TIMESTAMPLTZ = "TIMESTAMPLTZ"
    TIMESTAMPTZ = "TIMESTAMPTZ"
    TIMESTAMP = "TIMESTAMP"
    TABLE_SAMPLE = "TABLE_SAMPLE"
    PARAMETER = "PARAMETER"


@dataclass
class Token:
    token_type: TokenType
    text: str

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"Token({self.token_type}, {self.text!r})"


class Tokenizer:
    """
    Minimal tokenizer with support for SQL comments (including Snowflake //)
    and template comments {# ... #}.
    """

    # Defaults can be overridden by dialect Tokenizer subclasses
    KEYWORDS: Dict[str, TokenType] = {
        "SELECT": TokenType.SELECT,
    }

    SINGLE_TOKENS: Dict[str, TokenType] = {
        ",": TokenType.COMMA,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        "*": TokenType.STAR,
        ":": TokenType.COLON,
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "/": TokenType.DIV,
        ".": TokenType.DOT,
    }

    VAR_SINGLE_TOKENS: set = set()

    # Comments: single-line prefixes and block comment delimiters
    LINE_COMMENTS: Sequence[str] = ("--",)
    BLOCK_COMMENTS: Sequence[Tuple[str, str]] = (("/*", "*/"),)

    # Template comments like {# ... #} should always be recognized
    TEMPLATE_COMMENT_OPEN = "{#"
    TEMPLATE_COMMENT_CLOSE = "#}"

    QUOTES: Sequence[str] = ("'",)  # single-quoted strings
    STRING_ESCAPES: Sequence[str] = ("\\", "'")

    def __init__(self) -> None:
        pass

    # Public API ----------------------------------------------------------
    def tokenize(self, sql: str) -> List[Token]:
        tokens: List[Token] = []
        i = 0
        length = len(sql)

        while i < length:
            ch = sql[i]

            # Whitespace skip
            if ch.isspace():
                i += 1
                continue

            # Template comment
            if sql.startswith(self.TEMPLATE_COMMENT_OPEN, i):
                comment_text, i = self._consume_template_comment(sql, i)
                tokens.append(Token(TokenType.COMMENT, comment_text))
                continue

            # Block comments
            block_match = self._match_block_comment(sql, i)
            if block_match:
                comment_text, i = block_match
                tokens.append(Token(TokenType.COMMENT, comment_text))
                continue

            # Line comments (dialect-specific)
            line_match = self._match_line_comment(sql, i)
            if line_match:
                comment_text, i = line_match
                tokens.append(Token(TokenType.COMMENT, comment_text))
                continue

            # Numbers
            if ch.isdigit():
                num, i = self._consume_number(sql, i)
                tokens.append(Token(TokenType.NUMBER, num))
                continue

            # Strings
            if ch in self.QUOTES:
                s, i = self._consume_string(sql, i)
                tokens.append(Token(TokenType.STRING, s))
                continue

            # Identifiers / Keywords
            if ch.isalpha() or ch == "_":
                ident, i = self._consume_identifier(sql, i)
                token_type = self.KEYWORDS.get(ident.upper(), TokenType.IDENTIFIER)
                tokens.append(Token(token_type, ident))
                continue

            # Double-slash could be floordiv (non-Snowflake) or handled as comment by _match_line_comment above
            if ch == "/" and i + 1 < length and sql[i + 1] == "/":
                # If not treated as a comment by dialect, treat as FLOORDIV
                tokens.append(Token(TokenType.FLOORDIV, "//"))
                i += 2
                continue

            # Single-character tokens
            token_type = self.SINGLE_TOKENS.get(ch)
            if token_type:
                tokens.append(Token(token_type, ch))
                i += 1
                continue

            # Fallback: treat as identifier char sequence
            ident, i = self._consume_identifier(sql, i)
            token_type = self.KEYWORDS.get(ident.upper(), TokenType.IDENTIFIER)
            tokens.append(Token(token_type, ident))

        tokens.append(Token(TokenType.EOF, ""))
        return tokens

    # Internal helpers ----------------------------------------------------
    def _consume_number(self, sql: str, i: int) -> Tuple[str, int]:
        start = i
        length = len(sql)
        while i < length and sql[i].isdigit():
            i += 1
        return sql[start:i], i

    def _consume_identifier(self, sql: str, i: int) -> Tuple[str, int]:
        start = i
        length = len(sql)
        while i < length and (sql[i].isalnum() or sql[i] == "_"):
            i += 1
        return sql[start:i], i

    def _consume_string(self, sql: str, i: int) -> Tuple[str, int]:
        quote = sql[i]
        i += 1
        start = i
        buf = []
        length = len(sql)
        while i < length:
            ch = sql[i]
            if ch == quote:
                s = "".join(buf)
                i += 1
                return s, i
            if ch == "\\" and i + 1 < length:
                # simple escape handling
                i += 1
                buf.append(sql[i])
                i += 1
                continue
            buf.append(ch)
            i += 1
        # Unterminated string - capture what we have
        return "".join(buf), i

    def _consume_template_comment(self, sql: str, i: int) -> Tuple[str, int]:
        close = self.TEMPLATE_COMMENT_CLOSE
        end = sql.find(close, i + len(self.TEMPLATE_COMMENT_OPEN))
        if end == -1:
            end = len(sql)
        # include delimiters in text
        comment_text = sql[i : end + len(close)]
        return comment_text, end + len(close)

    def _match_line_comment(self, sql: str, i: int) -> Optional[Tuple[str, int]]:
        for prefix in self.LINE_COMMENTS:
            if sql.startswith(prefix, i):
                # consume until newline or end
                end = i + len(prefix)
                length = len(sql)
                while end < length and sql[end] not in "\r\n":
                    end += 1
                return sql[i:end], end
        return None

    def _match_block_comment(self, sql: str, i: int) -> Optional[Tuple[str, int]]:
        for start, end_delim in self.BLOCK_COMMENTS:
            if sql.startswith(start, i):
                end = sql.find(end_delim, i + len(start))
                if end == -1:
                    end = len(sql)
                    return sql[i:end], end
                return sql[i : end + len(end_delim)], end + len(end_delim)
        return None


__all__ = ["Tokenizer", "Token", "TokenType"]
