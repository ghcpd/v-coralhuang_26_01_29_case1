from __future__ import annotations

from typing import Any

from sqlglot import exp


class Generator:
    TRANSFORMS = {}
    TYPE_MAPPING = {}
    STAR_MAPPING = {}
    PROPERTIES_LOCATION = {}

    def sql(self, expression, key=None):  # pragma: no cover - stub
        return ""

    def func(self, name: str, *args):  # pragma: no cover - stub
        return f"{name}({', '.join(str(a) for a in args if a is not None)})"

    def function_fallback_sql(self, expression):  # pragma: no cover - stub
        return ""

    def format_time(self, expression):  # pragma: no cover - stub
        return ""

    def expressions(self, expression):  # pragma: no cover - stub
        return ""

    def unsupported(self, message: str):  # pragma: no cover - stub
        raise NotImplementedError(message)
