"""Stub expression module"""

class Expression:
    """Base expression class"""
    pass


# Stub expression classes
class ArrayAgg(Expression):
    @staticmethod
    def from_arg_list(args):
        return ArrayAgg()


class Array(Expression):
    @staticmethod
    def from_arg_list(args):
        return Array()


class ArrayJoin(Expression):
    @staticmethod
    def from_arg_list(args):
        return ArrayJoin()


class ArrayConcat(Expression):
    pass


class DateAdd(Expression):
    pass


class DateDiff(Expression):
    pass


class Anonymous(Expression):
    pass


class AtTimeZone(Expression):
    pass


class Extract(Expression):
    pass


class Cast(Expression):
    pass


class DataType(Expression):
    class Type:
        TIMESTAMP = "TIMESTAMP"
    
    @staticmethod
    def build(type_name):
        return DataType()


class TimeToUnix(Expression):
    pass


class Mul(Expression):
    pass


class Literal(Expression):
    @staticmethod
    def number(n):
        return Literal()


class EQ(Expression):
    pass


class Div(Expression):
    pass


class If(Expression):
    @staticmethod
    def from_arg_list(args):
        return If()


class Is(Expression):
    pass


class Null(Expression):
    pass


class StarMap(Expression):
    pass


class Struct(Expression):
    pass


class Condition(Expression):
    pass


class RegexpLike(Expression):
    @staticmethod
    def from_arg_list(args):
        return RegexpLike()


class Pow(Expression):
    pass


class ToChar(Expression):
    @staticmethod
    def from_arg_list(args):
        return ToChar()


class UnixToTime(Expression):
    SECONDS = "seconds"
    MILLIS = "millis"
    MICROS = "micros"
    
    @staticmethod
    def from_arg_list(args):
        return UnixToTime()


class StrToTime(Expression):
    pass


class SetTag(Expression):
    pass


class LikeAny(Expression):
    pass


class ILikeAny(Expression):
    pass


class DayOfWeek(Expression):
    pass


class LogicalAnd(Expression):
    pass


class LogicalOr(Expression):
    pass


class Map(Expression):
    pass


class Max(Expression):
    pass


class Min(Expression):
    pass


class PartitionedByProperty(Expression):
    pass


class Select(Expression):
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


class DateStrToDate(Expression):
    pass


class Except(Expression):
    pass


class Intersect(Expression):
    pass


class Describe(Expression):
    pass


class GeneratedAsIdentityColumnConstraint(Expression):
    pass


class SetProperty(Expression):
    pass


class VolatileProperty(Expression):
    pass


class Properties(Expression):
    class Location:
        UNSUPPORTED = "unsupported"


class Bracket(Expression):
    pass


def cast(expr, to_type):
    """Cast expression to type"""
    return Cast()
