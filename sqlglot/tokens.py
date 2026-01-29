from __future__ import annotations

import dataclasses
import enum
import typing as t


class TokenType(str, enum.Enum):
    SELECT = "SELECT"
    NUMBER = "NUMBER"
    SLASH = "/"
    COMMENT = "COMMENT"
    EOF = "EOF"


@dataclasses.dataclass(frozen=True)
class Token:
    token_type: TokenType
    text: str
    start: int
    end: int


class TokenizeError(ValueError):
    pass


class Tokenizer:
    """Minimal tokenizer with dialect-configurable comment rules.

    Supported:
    - `--` single-line
    - `/* ... */` block
    - dialect-specific single-line markers (e.g. Snowflake supports `//`)

    Additionally supports template comments `{# ... #}` in a dialect-agnostic way.
    """

    KEYWORDS = {"SELECT": TokenType.SELECT}

    def __init__(
        self,
        *,
        line_comment_starts: t.Sequence[str] = ("--",),
        block_comment_start: str = "/*",
        block_comment_end: str = "*/",
    ) -> None:
        self._line_comment_starts = tuple(sorted(line_comment_starts, key=len, reverse=True))
        self._block_comment_start = block_comment_start
        self._block_comment_end = block_comment_end

    def tokenize(self, sql: str) -> t.List[Token]:
        tokens: t.List[Token] = []
        i = 0
        n = len(sql)

        while i < n:
            ch = sql[i]

            # Whitespace
            if ch.isspace():
                i += 1
                continue

            # Template-style comment: `{# ... #}`
            # Must win over dialect overrides and normal symbol parsing.
            if sql.startswith("{#", i):
                end = sql.find("#}", i + 2)
                if end == -1:
                    raise TokenizeError("Unterminated template comment '{# ... #}'")
                end += 2
                tokens.append(Token(TokenType.COMMENT, sql[i:end], i, end))
                i = end
                continue

            # Block comment: `/* ... */`
            if self._block_comment_start and sql.startswith(self._block_comment_start, i):
                end = sql.find(self._block_comment_end, i + len(self._block_comment_start))
                if end == -1:
                    raise TokenizeError("Unterminated block comment")
                end += len(self._block_comment_end)
                tokens.append(Token(TokenType.COMMENT, sql[i:end], i, end))
                i = end
                continue

            # Single-line comments (dialect-configurable)
            matched_line = None
            for marker in self._line_comment_starts:
                if marker and sql.startswith(marker, i):
                    matched_line = marker
                    break
            if matched_line is not None:
                start = i
                i += len(matched_line)
                while i < n and sql[i] not in "\r\n":
                    i += 1
                tokens.append(Token(TokenType.COMMENT, sql[start:i], start, i))
                continue

            # Number
            if ch.isdigit():
                start = i
                i += 1
                while i < n and sql[i].isdigit():
                    i += 1
                tokens.append(Token(TokenType.NUMBER, sql[start:i], start, i))
                continue

            # Identifier/keyword
            if ch.isalpha() or ch == "_":
                start = i
                i += 1
                while i < n and (sql[i].isalnum() or sql[i] == "_"):
                    i += 1
                raw = sql[start:i]
                upper = raw.upper()
                token_type = self.KEYWORDS.get(upper)
                if token_type is None:
                    raise TokenizeError(f"Unsupported identifier {raw!r}")
                tokens.append(Token(token_type, raw, start, i))
                continue

            # Operators
            if ch == "/":
                tokens.append(Token(TokenType.SLASH, ch, i, i + 1))
                i += 1
                continue

            raise TokenizeError(f"Unexpected character {ch!r} at position {i}")

        tokens.append(Token(TokenType.EOF, "", n, n))
        return tokens
