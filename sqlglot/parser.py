from __future__ import annotations

import typing as t

from .expressions import Div, Literal, Select, Expression
from .tokens import Token, TokenType, TokenizeError
from . import dialects


class ParseError(ValueError):
    pass


def _dialect_from_read(read: t.Union[str, type, None]) -> type:
    if read is None:
        return dialects.Dialect

    if isinstance(read, str):
        key = read.lower()
        if key == "snowflake":
            return dialects.Snowflake
        if key in ("postgres", "postgresql"):
            return dialects.Postgres
        raise ValueError(f"Unknown dialect: {read}")

    if isinstance(read, type):
        return read

    raise TypeError("read must be None, a dialect name, or a Dialect class")


class Parser:
    def __init__(self, tokens: t.Sequence[Token]) -> None:
        self._tokens = tokens
        self._i = 0

    def _current(self) -> Token:
        return self._tokens[self._i]

    def _advance(self) -> Token:
        tok = self._tokens[self._i]
        self._i += 1
        return tok

    def _match(self, token_type: TokenType) -> bool:
        if self._current().token_type == token_type:
            self._advance()
            return True
        return False

    def _expect(self, token_type: TokenType) -> Token:
        if self._current().token_type != token_type:
            raise ParseError(f"Expected {token_type}, found {self._current().token_type}")
        return self._advance()

    def parse(self) -> Select:
        self._expect(TokenType.SELECT)
        expr = self._parse_expression()
        self._expect(TokenType.EOF)
        return Select(expressions=(expr,))

    def _parse_expression(self) -> Expression:
        left = self._parse_primary()
        while self._match(TokenType.SLASH):
            right = self._parse_primary()
            left = Div(left=left, right=right)
        return left

    def _parse_primary(self) -> Expression:
        tok = self._current()
        if tok.token_type == TokenType.NUMBER:
            self._advance()
            return Literal(int(tok.text))
        raise ParseError(f"Expected primary expression, found {tok.token_type}")


def parse_one(sql: str, *, read: t.Union[str, type, None] = None) -> Select:
    dialect = _dialect_from_read(read)
    tokenizer = dialect.tokenizer()

    try:
        tokens = tokenizer.tokenize(sql)
    except TokenizeError as e:
        raise ParseError(str(e)) from e

    # Comments must not affect AST construction
    tokens_wo_comments = [t for t in tokens if t.token_type != TokenType.COMMENT]
    return Parser(tokens_wo_comments).parse()
