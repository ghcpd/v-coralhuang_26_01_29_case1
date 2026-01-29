from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional


class Expression:
    """Minimal expression base class."""

    def sql(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.sql()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Expression) and self.sql() == other.sql()


@dataclass
class Literal(Expression):
    this: str
    is_string: bool = False

    @property
    def name(self) -> str:
        return self.this

    def sql(self) -> str:
        return f"'{self.this}'" if self.is_string else self.this

    @staticmethod
    def number(value: Any) -> "Literal":
        return Literal(str(value), is_string=False)


@dataclass
class Identifier(Expression):
    this: str

    def sql(self) -> str:
        return self.this


@dataclass
class Select(Expression):
    expressions: List[Expression] = field(default_factory=list)

    def sql(self) -> str:
        expr_sql = ", ".join(expr.sql() for expr in self.expressions) if self.expressions else ""
        return f"SELECT {expr_sql}".rstrip()


# Additional stub expressions used by snowflake.py (unused in our tests but required for imports)
@dataclass
class Array(Expression):
    expressions: List[Expression] = field(default_factory=list)

    @staticmethod
    def from_arg_list(args: List[Expression]) -> "Array":
        return Array(expressions=args)

    def sql(self) -> str:
        return f"ARRAY[{', '.join(e.sql() for e in self.expressions)}]"


class ArrayAgg(Expression):
    @staticmethod
    def from_arg_list(args: List[Expression]) -> "ArrayAgg":
        return ArrayAgg()

    def sql(self) -> str:
        return "ARRAY_AGG(...)"


class ArrayJoin(Expression):
    @staticmethod
    def from_arg_list(args: List[Expression]) -> "ArrayJoin":
        return ArrayJoin()

    def sql(self) -> str:
        return "ARRAY_JOIN(...)"


class Anonymous(Expression):
    def __init__(self, this: str, expressions: Optional[List[Expression]] = None):
        self.this = this
        self.expressions = expressions or []

    def sql(self) -> str:
        return f"{self.this}({', '.join(e.sql() for e in self.expressions)})"


class DateAdd(Expression):
    def __init__(self, this: Expression, expression: Expression, unit: Expression):
        self.args = {"this": this, "expression": expression, "unit": unit}

    def sql(self) -> str:
        return f"DATEADD({self.args['unit'].sql()}, {self.args['expression'].sql()}, {self.args['this'].sql()})"


class DateDiff(Expression):
    def __init__(self, this: Expression, expression: Expression, unit: Expression):
        self.args = {"this": this, "expression": expression, "unit": unit}

    def sql(self) -> str:
        return f"DATEDIFF({self.args['unit'].sql()}, {self.args['expression'].sql()}, {self.args['this'].sql()})"


class Struct(Expression):
    def __init__(self, expressions: List[Expression]):
        self.expressions = expressions

    def sql(self) -> str:
        return f"STRUCT({', '.join(e.sql() for e in self.expressions)})"


class StarMap(Expression):
    def sql(self) -> str:
        return "STARMAP"


class Condition(Expression):
    def eq(self, other: Expression) -> Expression:
        return Anonymous("=", [self, other])


class UnixToTime(Expression):
    SECONDS = "SECONDS"
    MILLIS = "MILLIS"
    MICROS = "MICROS"

    def __init__(self, this: Expression, scale: Optional[str] = None):
        self.args = {"this": this, "scale": scale}

    @staticmethod
    def from_arg_list(args: List[Expression]) -> "UnixToTime":
        this = args[0] if args else Literal.number(0)
        scale = args[1] if len(args) > 1 else None
        return UnixToTime(this, scale=scale if isinstance(scale, str) else None)

    def sql(self) -> str:
        return f"UNIX_TO_TIME({self.args['this'].sql()})"


class StrToTime(Expression):
    def __init__(self, this: Expression, **kwargs):
        self.args = {"this": this, **kwargs}

    def sql(self) -> str:
        return f"STR_TO_TIME({self.args['this'].sql()})"


class TimeToUnix(Expression):
    def __init__(self, this: Expression):
        self.args = {"this": this}

    def sql(self) -> str:
        return f"TIME_TO_UNIX({self.args['this'].sql()})"


class Extract(Expression):
    def __init__(self, this: Expression, expression: Expression):
        self.args = {"this": this, "expression": expression}

    def sql(self) -> str:
        return f"EXTRACT({self.args['this'].sql()} FROM {self.args['expression'].sql()})"


class If(Expression):
    def __init__(self, this: Expression, true: Expression, false: Expression):
        self.args = {"this": this, "true": true, "false": false}

    @staticmethod
    def from_arg_list(args: List[Expression]) -> "If":
        cond, true, false = args
        return If(cond, true, false)

    def sql(self) -> str:
        return f"IF({self.args['this'].sql()}, {self.args['true'].sql()}, {self.args['false'].sql()})"


class Mul(Expression):
    def __init__(self, this: Expression, expression: Expression):
        self.args = {"this": this, "expression": expression}

    def sql(self) -> str:
        return f"({self.args['this'].sql()} * {self.args['expression'].sql()})"


class Pow(Expression):
    def __init__(self, this: Expression, expression: Expression):
        self.args = {"this": this, "expression": expression}

    def sql(self) -> str:
        return f"POWER({self.args['this'].sql()}, {self.args['expression'].sql()})"


class RegexpLike(Expression):
    @staticmethod
    def from_arg_list(args: List[Expression]) -> "RegexpLike":
        return RegexpLike()

    def sql(self) -> str:
        return "REGEXP_LIKE(...)"


class ToChar(Expression):
    @staticmethod
    def from_arg_list(args: List[Expression]) -> "ToChar":
        return ToChar()

    def sql(self) -> str:
        return "TO_CHAR(...)"


class DataType(Expression):
    class Type:
        TIMESTAMP = "TIMESTAMP"
        ARRAY = "ARRAY"
        MAP = "MAP"

    def __init__(self, this: str):
        self.this = this

    def is_type(self, t: str) -> bool:
        return self.this.lower() == t

    def sql(self) -> str:
        return self.this


# Stub others to satisfy imports (no-op implementations)
class Map(Expression):
    def sql(self) -> str:
        return "MAP(...)"


class VarMap(Expression):
    def sql(self) -> str:
        return "VAR_MAP(...)"


class Star(Expression):
    def sql(self) -> str:
        return "*"


class AtTimeZone(Expression):
    def __init__(self, this: Expression, zone: Expression):
        self.args = {"this": this, "zone": zone}

    def sql(self) -> str:
        return f"AT_TIME_ZONE({self.args['this'].sql()}, {self.args['zone'].sql()})"


# Simple Null expression
class Null(Expression):
    def sql(self) -> str:
        return "NULL"


class Is(Expression):
    def __init__(self, this: Expression, expression: Expression):
        self.args = {"this": this, "expression": expression}

    def sql(self) -> str:
        return f"{self.args['this'].sql()} IS {self.args['expression'].sql()}"


class EQ(Expression):
    def __init__(self, this: Expression, expression: Expression):
        self.args = {"this": this, "expression": expression}

    def sql(self) -> str:
        return f"{self.args['this'].sql()} = {self.args['expression'].sql()}"


__all__ = [
    "Expression",
    "Literal",
    "Identifier",
    "Select",
    "Array",
    "ArrayAgg",
    "ArrayJoin",
    "Anonymous",
    "DateAdd",
    "DateDiff",
    "Struct",
    "StarMap",
    "Condition",
    "UnixToTime",
    "StrToTime",
    "TimeToUnix",
    "Extract",
    "If",
    "Mul",
    "Pow",
    "RegexpLike",
    "ToChar",
    "DataType",
    "Map",
    "VarMap",
    "Star",
    "AtTimeZone",
    "Null",
    "Is",
    "EQ",
]
