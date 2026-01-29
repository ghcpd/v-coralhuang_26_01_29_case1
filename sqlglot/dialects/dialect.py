from __future__ import annotations

from typing import Type

from ..parser import Parser as BaseParser
from ..tokenizer import Tokenizer as BaseTokenizer


class Dialect:
    Parser: Type[BaseParser] = BaseParser
    Tokenizer: Type[BaseTokenizer] = BaseTokenizer

    @classmethod
    def tokenize(cls, sql: str):
        return cls.Tokenizer(sql).tokens()

    @classmethod
    def parse(cls, sql: str):
        tokens = cls.tokenize(sql)
        parser = cls.Parser(tokens)
        return parser.parse()

__all__ = ["Dialect"]
