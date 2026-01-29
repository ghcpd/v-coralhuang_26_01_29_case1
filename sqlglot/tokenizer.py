from __future__ import annotations

import re
from typing import Dict, Iterable, List, Tuple

from .tokens import (
    DEFAULT_BLOCK_COMMENT_DELIMS,
    DEFAULT_KEYWORDS,
    DEFAULT_LINE_COMMENT_PREFIXES,
    DEFAULT_SINGLE_TOKENS,
    DEFAULT_TEMPLATE_COMMENT_DELIM,
    Token,
    TokenType,
)


class Tokenizer:
    """
    Minimal tokenizer with comment awareness.

    Dialects can override class attributes to customize behavior.
    Template comments `{# ... #}` are always recognized independent of dialect overrides.
    """

    # String literal configuration
    QUOTES: List[str] = ["'"]
    STRING_ESCAPES: List[str] = ["\\", "'"]

    # Keyword and symbol configuration
    KEYWORDS: Dict[str, TokenType] = DEFAULT_KEYWORDS.copy()
    SINGLE_TOKENS: Dict[str, TokenType] = DEFAULT_SINGLE_TOKENS.copy()
    VAR_SINGLE_TOKENS: Tuple[str, ...] = ()  # tokens that can repeat like $$

    # Comment configuration (dialect-specific)
    LINE_COMMENT_PREFIXES: Tuple[str, ...] = DEFAULT_LINE_COMMENT_PREFIXES
    BLOCK_COMMENT_DELIMS: Tuple[Tuple[str, str], ...] = DEFAULT_BLOCK_COMMENT_DELIMS

    # Template comments (always enabled)
    TEMPLATE_COMMENT_DELIM: Tuple[str, str] = DEFAULT_TEMPLATE_COMMENT_DELIM

    def __init__(self, sql: str):
        self.sql = sql
        self.length = len(sql)
        self.position = 0

    def _match_at(self, s: str) -> bool:
        return self.sql.startswith(s, self.position)

    def _consume(self, n: int):
        self.position += n

    def _peek(self, n: int = 0) -> str:
        pos = self.position + n
        return self.sql[pos] if pos < self.length else ""

    def tokens(self) -> List[Token]:
        tokens: List[Token] = []
        while self.position < self.length:
            ch = self._peek()

            # Whitespace skip
            if ch.isspace():
                self._consume(1)
                continue

            # Template comments {# ... #}
            start_tpl, end_tpl = self.TEMPLATE_COMMENT_DELIM
            if self._match_at(start_tpl):
                end_idx = self.sql.find(end_tpl, self.position + len(start_tpl))
                if end_idx == -1:
                    # Consume rest if no closing; still treat as comment
                    comment_text = self.sql[self.position :]
                    self.position = self.length
                else:
                    comment_text = self.sql[self.position : end_idx + len(end_tpl)]
                    self.position = end_idx + len(end_tpl)
                tokens.append(Token(TokenType.COMMENT, comment_text))
                continue

            # Block comments /* ... */
            matched_block = False
            for start, end in self.BLOCK_COMMENT_DELIMS:
                if self._match_at(start):
                    matched_block = True
                    end_idx = self.sql.find(end, self.position + len(start))
                    if end_idx == -1:
                        comment_text = self.sql[self.position :]
                        self.position = self.length
                    else:
                        comment_text = self.sql[self.position : end_idx + len(end)]
                        self.position = end_idx + len(end)
                    tokens.append(Token(TokenType.COMMENT, comment_text))
                    break
            if matched_block:
                continue

            # Line comments (--, //, etc) - check longest prefix first
            if self.LINE_COMMENT_PREFIXES:
                matched_prefix = None
                for prefix in sorted(self.LINE_COMMENT_PREFIXES, key=len, reverse=True):
                    if self._match_at(prefix):
                        matched_prefix = prefix
                        break
                if matched_prefix:
                    start_pos = self.position
                    # consume until newline or EOF
                    while self.position < self.length and self._peek() not in "\r\n":
                        self._consume(1)
                    comment_text = self.sql[start_pos:self.position]
                    tokens.append(Token(TokenType.COMMENT, comment_text))
                    continue

            # Strings
            if ch in self.QUOTES:
                quote = ch
                start_pos = self.position
                self._consume(1)  # consume opening quote
                while self.position < self.length:
                    cur = self._peek()
                    if cur == quote:
                        self._consume(1)
                        break
                    if cur == "" :
                        break
                    # Handle escape sequences
                    if cur in self.STRING_ESCAPES:
                        # consume escape and next char if any
                        self._consume(1)
                        if self.position < self.length:
                            self._consume(1)
                            continue
                    else:
                        self._consume(1)
                text = self.sql[start_pos:self.position]
                tokens.append(Token(TokenType.STRING, text))
                continue

            # Numbers (simple integer)
            if ch.isdigit():
                start_pos = self.position
                while self._peek().isdigit():
                    self._consume(1)
                text = self.sql[start_pos:self.position]
                tokens.append(Token(TokenType.NUMBER, text))
                continue

            # Identifiers / keywords
            if ch.isalpha() or ch == "_":
                start_pos = self.position
                while self._peek().isalnum() or self._peek() == "_":
                    self._consume(1)
                text = self.sql[start_pos:self.position]

                # Attempt to match multi-word keywords greedily (e.g. LIKE ANY)
                matched = None
                # Check combined with next token(s) by peeking ahead in raw string
                # Build a slice from current position to look for patterns like " LIKE ANY"
                if self.KEYWORDS:
                    remaining = self.sql[self.position:]
                    # Sort keys by length to match longest first
                    for kw in sorted(self.KEYWORDS.keys(), key=len, reverse=True):
                        if " " in kw:
                            composite = text.upper() + remaining[: len(kw) - len(text)]
                            if composite.upper().startswith(kw):
                                matched = kw
                                # consume extra characters beyond first word
                                extra_len = len(kw) - len(text)
                                self._consume(extra_len)
                                text = kw  # normalized
                                break
                    if matched is None:
                        matched = text.upper()

                lookup_key = matched if matched is not None else text.upper()
                token_type = self.KEYWORDS.get(lookup_key, TokenType.IDENTIFIER)
                tokens.append(Token(token_type, text))
                continue

            # Single-character tokens
            token_type = self.SINGLE_TOKENS.get(ch)
            if token_type:
                tokens.append(Token(token_type, ch))
                self._consume(1)
                continue

            # Unknown token, consume one char to avoid infinite loop
            tokens.append(Token(TokenType.UNKNOWN, ch))
            self._consume(1)

        tokens.append(Token(TokenType.EOF, ""))
        return tokens


__all__ = ["Tokenizer"]
