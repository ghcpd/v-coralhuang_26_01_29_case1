from __future__ import annotations

from typing import Callable, Sequence


def preprocess(funcs: Sequence[Callable]):  # pragma: no cover - stub
    def _inner(expression):
        for f in funcs:
            expression = f(expression)
        return expression

    return _inner


def eliminate_distinct_on(expression):  # pragma: no cover - stub
    return expression
