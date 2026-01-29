from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional, Sequence, Tuple, Type


@dataclass
class Expression:
    args: Dict[str, Any] = field(default_factory=dict)

    def __eq__(self, other: Any) -> bool:
        return self.__class__ is other.__class__ and self.args == getattr(other, "args", None)

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        cls = self.__class__.__name__
        return f"{cls}({self.args})"

    # Helper for binary expressions
    @property
    def this(self):
        return self.args.get("this")

    @property
    def expression(self):
        return self.args.get("expression")


class Literal(Expression):
    def __init__(self, this: str, is_string: bool = False):
        super().__init__({"this": this, "is_string": is_string})

    @staticmethod
    def number(value: str) -> "Literal":
        return Literal(value, is_string=False)

    @staticmethod
    def string(value: str) -> "Literal":
        return Literal(value, is_string=True)

    @property
    def is_string(self) -> bool:
        return bool(self.args.get("is_string"))

    @property
    def name(self) -> str:
        # name is used in snowflake `_snowflake_to_timestamp`
        return str(self.args.get("this"))


class Identifier(Expression):
    def __init__(self, this: str):
        super().__init__({"this": this})


class Star(Expression):
    pass


class Select(Expression):
    def __init__(self, expressions: Sequence[Expression]):
        super().__init__({"expressions": list(expressions)})

    @property
    def expressions(self) -> List[Expression]:
        return self.args.get("expressions", [])


# Binary helper expressions -------------------------------------------------
class Binary(Expression):
    def __init__(self, this=None, expression=None):
        super().__init__({"this": this, "expression": expression})


class EQ(Binary):
    pass


class Mul(Binary):
    pass


class Div(Binary):
    pass


class Pow(Binary):
    pass


class Is(Binary):
    pass


class If(Expression):
    @classmethod
    def from_arg_list(cls, args):
        # Expect [condition, true, false]
        return cls({"args": args})

    def __init__(self, this=None, true=None, false=None, **kwargs):
        args = kwargs if kwargs else {"this": this, "true": true, "false": false}
        super().__init__(args)


class Null(Expression):
    pass


class Extract(Binary):
    pass


class TimeToUnix(Expression):
    pass


class StrToTime(Expression):
    pass


class UnixToTime(Expression):
    SECONDS: ClassVar[str] = "seconds"
    MILLIS: ClassVar[str] = "millis"
    MICROS: ClassVar[str] = "micros"

    def __init__(self, this=None, scale=None):
        super().__init__({"this": this, "scale": scale})

    @classmethod
    def from_arg_list(cls, args):
        # naive mapping: first arg is 'this'
        return cls(this=args[0] if args else None)


class DateAdd(Binary):
    pass


class DateDiff(Binary):
    pass


class Array(Expression):
    @classmethod
    def from_arg_list(cls, args):
        return cls({"expressions": args})


class ArrayAgg(Expression):
    @classmethod
    def from_arg_list(cls, args):
        return cls({"expressions": args})


class ArrayJoin(Expression):
    @classmethod
    def from_arg_list(cls, args):
        return cls({"expressions": args})


class RegexpLike(Expression):
    @classmethod
    def from_arg_list(cls, args):
        return cls({"expressions": args})


class ToChar(Expression):
    @classmethod
    def from_arg_list(cls, args):
        return cls({"expressions": args})


class Struct(Expression):
    def __init__(self, expressions=None):
        super().__init__({"expressions": expressions or []})

    @property
    def expressions(self):
        return self.args.get("expressions", [])


class Condition(Expression):
    def eq(self, other):
        return EQ(this=self, expression=other)


class StarMap(Expression):
    pass


class Map(Expression):
    pass


class DataType(Expression):
    class Type:
        TIMESTAMP = "TIMESTAMP"
        ARRAY = "ARRAY"
        MAP = "MAP"

    def __init__(self, this=None):
        super().__init__({"this": this})

    def is_type(self, name: str) -> bool:
        return str(self.args.get("this")).lower() == name.lower()

    @staticmethod
    def build(name: str) -> "DataType":
        return DataType(name)


class DayOfWeek(Expression):
    pass


class LogicalAnd(Expression):
    pass


class LogicalOr(Expression):
    pass


class PartitionedByProperty(Expression):
    pass


class StrPosition(Expression):
    pass


class TimeStrToTime(Expression):
    pass


class TimeToStr(Expression):
    pass


class TimestampTrunc(Expression):
    pass


class Trim(Expression):
    pass


class TsOrDsToDate(Expression):
    pass


class VarMap(Expression):
    pass


class AtTimeZone(Expression):
    pass


class SelectProperty(Expression):
    pass


class SetTag(Expression):
    pass


class Describe(Expression):
    pass


class GeneratedAsIdentityColumnConstraint(Expression):
    pass


class ArrayConcat(Expression):
    pass


class Max(Expression):
    pass


class Min(Expression):
    pass


class DateStrToDate(Expression):
    pass


class Anonymous(Expression):
    @classmethod
    def from_arg_list(cls, args):
        return cls({"expressions": args})


class Cast(Expression):
    def __init__(self, this=None, to=None):
        super().__init__({"this": this, "to": to})


class IdentifierList(Expression):
    pass


class Bracket(Expression):
    def __init__(self, this=None, expressions=None):
        super().__init__({"this": this, "expressions": expressions or []})


class LikeAny(Expression):
    pass


class ILikeAny(Expression):
    pass


class Except(Expression):
    pass


class Intersect(Expression):
    pass


class SetProperty(Expression):
    pass


class VolatileProperty(Expression):
    pass


class Properties:
    class Location:
        UNSUPPORTED = "UNSUPPORTED"


# Convenience helper

def cast(this, to):
    return Cast(this=this, to=to)


# Convenience alias for compatibility in exp.py
__all__ = [name for name in globals() if not name.startswith("_")]
