from __future__ import annotations

from ..tokenizer import Tokenizer
from ..parser import Parser


class Dialect:
    """Base dialect: uses default tokenizer and parser."""

    Tokenizer = Tokenizer
    Parser = Parser


__all__ = ["Dialect"]
