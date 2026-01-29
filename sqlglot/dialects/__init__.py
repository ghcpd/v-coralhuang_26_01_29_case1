from __future__ import annotations

from typing import Union, Type

from .dialect import Dialect
from .snowflake import Snowflake


dialects = {
    "ansi": Dialect,
    "snowflake": Snowflake,
    "snow": Snowflake,
}


def get_dialect(name: Union[str, Type[Dialect], None]):
    if name is None:
        return Dialect
    if isinstance(name, str):
        key = name.lower()
        return dialects.get(key, Dialect)
    if isinstance(name, type) and issubclass(name, Dialect):
        return name
    return Dialect

__all__ = ["Dialect", "Snowflake", "get_dialect", "dialects"]
