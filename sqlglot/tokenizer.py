from __future__ import annotations

from typing import List

from .tokens import Token, TokenType


class Tokenizer:
    """Simple SQL tokenizer with comment support."""

    # Default comment specs: -- and /* */
    COMMENT_SPEC = [("--", "\n"), ("/*", "*/")]
    TEMPLATE_COMMENT = ("{#", "#}")

    def __init__(self, sql: str):
        self.sql = sql

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        s = self.sql
        n = len(s)
        i = 0

        while i < n:
            ch = s[i]

            # Whitespace
            if ch.isspace():
                i += 1
                continue

            # Template comment (highest priority)
            if s.startswith(self.TEMPLATE_COMMENT[0], i):
                end = s.find(self.TEMPLATE_COMMENT[1], i + len(self.TEMPLATE_COMMENT[0]))
                if end == -1:
                    end = n
                    text = s[i:end]
                else:
                    end += len(self.TEMPLATE_COMMENT[1])
                    text = s[i:end]
                tokens.append(Token(TokenType.COMMENT, text))
                i = end
                continue

            # Dialect-specific comments
            matched_comment = False
            for start, end_marker in self.COMMENT_SPEC:
                if s.startswith(start, i):
                    if end_marker == "\n":
                        end = s.find("\n", i + len(start))
                        if end == -1:
                            end = n
                    else:
                        end = s.find(end_marker, i + len(start))
                        if end == -1:
                            end = n
                        else:
                            end += len(end_marker)
                    text = s[i:end]
                    tokens.append(Token(TokenType.COMMENT, text))
                    i = end
                    matched_comment = True
                    break
            if matched_comment:
                continue

            # Number literal
            if ch.isdigit():
                j = i + 1
                while j < n and s[j].isdigit():
                    j += 1
                tokens.append(Token(TokenType.NUMBER, s[i:j]))
                i = j
                continue

            # Identifier / keyword
            if ch.isalpha() or ch == "_":
                j = i + 1
                while j < n and (s[j].isalnum() or s[j] == "_"):
                    j += 1
                text = s[i:j]
                upper = text.upper()
                if upper in {"SELECT", "FROM"}:
                    tokens.append(Token(TokenType.KEYWORD, upper))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, text))
                i = j
                continue

            # Single-character tokens
            if ch == "*":
                tokens.append(Token(TokenType.STAR, ch))
                i += 1
                continue
            if ch == ",":
                tokens.append(Token(TokenType.COMMA, ch))
                i += 1
                continue

            # Fallback: treat as identifier (covers operators for this minimal parser)
            tokens.append(Token(TokenType.IDENTIFIER, ch))
            i += 1

        tokens.append(Token(TokenType.EOF, ""))
        return tokens


def tokenize(sql: str, tokenizer_cls: type[Tokenizer] | None = None) -> List[Token]:
    tokenizer_cls = tokenizer_cls or Tokenizer
    return tokenizer_cls(sql).tokenize()
