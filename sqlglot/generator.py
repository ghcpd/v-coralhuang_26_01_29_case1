from __future__ import annotations

from typing import Dict, Callable

from .expressions import Expression


class Generator:
    TRANSFORMS: Dict[type, Callable] = {}
    TYPE_MAPPING = {}
    STAR_MAPPING = {}
    PROPERTIES_LOCATION = {}
    PARAMETER_TOKEN = "?"
    MATCHED_BY_SOURCE = True
    SINGLE_STRING_INTERVAL = False
    JOIN_HINTS = True
    TABLE_HINTS = True

    def sql(self, expression: Expression, key: str = "this") -> str:
        # Minimal passthrough: assume expression is already Expression
        return expression.sql() if isinstance(expression, Expression) else str(expression)

    def datatype_sql(self, expression: Expression) -> str:
        return expression.sql()

    def expressions(self, *args, **kwargs):
        return ""

    def unsupported(self, message: str):
        raise NotImplementedError(message)

    def expression_sql(self, expression: Expression) -> str:
        return expression.sql()


__all__ = ["Generator"]
