from __future__ import annotations

from typing import Callable, List


def preprocess(funcs: List[Callable]) -> Callable:
    def wrapper(*args, **kwargs):
        return None

    return wrapper


def eliminate_distinct_on(*args, **kwargs):
    return None

__all__ = ["preprocess", "eliminate_distinct_on"]
