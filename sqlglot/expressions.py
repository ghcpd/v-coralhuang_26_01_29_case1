from __future__ import annotations

from dataclasses import dataclass
from typing import List


class Expression:
    """Base expression node."""

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Expression) and str(self) == str(other)

    def __repr__(self) -> str:
        return str(self)


@dataclass
class Literal(Expression):
    value: str

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Literal) and self.value == other.value


@dataclass
class Identifier(Expression):
    name: str

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Identifier) and self.name == other.name


@dataclass
class Select(Expression):
    expressions: List[Expression]

    def __str__(self) -> str:
        return "SELECT " + ", ".join(str(e) for e in self.expressions)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Select) and self.expressions == other.expressions
