from __future__ import annotations

import dataclasses
import typing as t


class Expression:
    def walk(self) -> t.Iterable["Expression"]:
        yield self


@dataclasses.dataclass(frozen=True)
class Literal(Expression):
    value: int


@dataclasses.dataclass(frozen=True)
class Div(Expression):
    left: Expression
    right: Expression

    def walk(self) -> t.Iterable[Expression]:
        yield self
        yield from self.left.walk()
        yield from self.right.walk()


@dataclasses.dataclass(frozen=True)
class Select(Expression):
    expressions: t.Tuple[Expression, ...]

    def walk(self) -> t.Iterable[Expression]:
        yield self
        for e in self.expressions:
            yield from e.walk()
