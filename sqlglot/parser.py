from __future__ import annotations

from typing import List

from .tokens import Token, TokenType
from .expressions import Select, Literal, Identifier, Expression


class Parser:
    """Very small SQL parser sufficient for the tests."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _current(self) -> Token:
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def _skip_comments(self) -> None:
        while self._current().type == TokenType.COMMENT:
            self._advance()

    def parse(self) -> Expression:
        self._skip_comments()
        tok = self._current()
        if tok.type == TokenType.KEYWORD and tok.text == "SELECT":
            return self._parse_select()
        raise ValueError(f"Unsupported query: {tok}")

    def _parse_select(self) -> Select:
        # consume SELECT
        self._advance()
        expressions: List[Expression] = []

        while True:
            self._skip_comments()
            tok = self._current()
            if tok.type == TokenType.EOF:
                break
            if tok.type == TokenType.COMMA:
                self._advance()
                continue

            expressions.append(self._parse_expression())

            # accept trailing comments and commas
            self._skip_comments()
            tok = self._current()
            if tok.type == TokenType.COMMA:
                self._advance()
                continue
            if tok.type == TokenType.EOF:
                break

        return Select(expressions=expressions)

    def _parse_expression(self) -> Expression:
        self._skip_comments()
        tok = self._current()
        if tok.type == TokenType.NUMBER:
            self._advance()
            return Literal(tok.text)
        if tok.type == TokenType.STAR:
            self._advance()
            return Identifier("*")
        if tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
            self._advance()
            return Identifier(tok.text)
        raise ValueError(f"Unexpected token in expression: {tok}")


def parse_one(sql: str, read=None):
    # Lazy import to avoid circular dependency
    from .dialects import get_dialect

    dialect = get_dialect(read)
    tokens = dialect.Tokenizer(sql).tokenize()
    parser = dialect.Parser(tokens)
    return parser.parse()
