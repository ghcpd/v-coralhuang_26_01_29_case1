from __future__ import annotations

from typing import Callable, Dict, List, Optional, Tuple, Type

from .expressions import Identifier, Literal, Select, Expression
from .tokenizer import Tokenizer
from .tokens import Token, TokenType


def binary_range_parser(cls: Type[Expression]) -> Callable:
    def _parser(self, this, expression):
        return cls()

    return _parser


class Parser:
    """Minimal parser that can parse simple SELECT statements and ignore comments."""

    FUNCTIONS: Dict[str, Callable] = {}
    FUNCTION_PARSERS: Dict[str, Callable] = {}
    FUNC_TOKENS = set()
    COLUMN_OPERATORS = {}
    TIMESTAMPS = {TokenType.TIME}
    RANGE_PARSERS: Dict[TokenType, Callable] = {}
    ALTER_PARSERS: Dict[str, Callable] = {}

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.position]

    def _advance(self) -> Token:
        tok = self.tokens[self.position]
        self.position += 1
        return tok

    def _match(self, token_type: TokenType) -> bool:
        if self.current.token_type == token_type:
            self._advance()
            return True
        return False

    def _skip_comments(self):
        while self.current.token_type == TokenType.COMMENT:
            self._advance()

    def parse(self) -> List[Expression]:
        expressions: List[Expression] = []
        while self.current.token_type != TokenType.EOF:
            self._skip_comments()
            if self.current.token_type == TokenType.EOF:
                break
            expr = self._parse_statement()
            if expr:
                expressions.append(expr)
            else:
                # fail fast
                raise SyntaxError(f"Unexpected token: {self.current}")
        return expressions

    def _parse_statement(self) -> Optional[Expression]:
        if self._match(TokenType.SELECT):
            return self._parse_select()
        return None

    def _parse_select(self) -> Select:
        expressions: List[Expression] = []
        self._skip_comments()
        # Parse a comma-separated list of simple expressions (numbers or identifiers)
        while self.current.token_type not in (TokenType.EOF,):
            if self.current.token_type == TokenType.COMMENT:
                self._skip_comments()
                continue
            if self.current.token_type in (TokenType.COMMA,):
                self._advance()
                continue
            if self.current.token_type == TokenType.NUMBER:
                lit = Literal(self.current.text)
                expressions.append(lit)
                self._advance()
            elif self.current.token_type == TokenType.STRING:
                lit = Literal(self.current.text.strip("'"), is_string=True)
                expressions.append(lit)
                self._advance()
            elif self.current.token_type == TokenType.IDENTIFIER:
                ident = Identifier(self.current.text)
                expressions.append(ident)
                self._advance()
            else:
                break
        return Select(expressions=expressions)


__all__ = ["Parser", "binary_range_parser"]
