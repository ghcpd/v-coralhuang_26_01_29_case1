from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    COMMENT = auto()
    KEYWORD = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STAR = auto()
    COMMA = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    text: str

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.text!r})"
