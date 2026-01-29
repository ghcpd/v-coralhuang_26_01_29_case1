"""
Dialects registry for the minimal sqlglot implementation.
"""
from __future__ import annotations

from typing import Dict, Type

from .dialect import Dialect
from typing import Dict, Type

# Registry of available dialect classes
_dialect_registry: Dict[str, Type[Dialect]] = {
    # default/ansi fallback
    "ansi": Dialect,
}


def _ensure_snowflake_loaded():
    if "snowflake" not in _dialect_registry:
        from . import snowflake  # local import to avoid circular dependency

        _dialect_registry["snowflake"] = snowflake.Snowflake


def get(name: str) -> Type[Dialect]:
    if name.lower() == "snowflake":
        _ensure_snowflake_loaded()
    return _dialect_registry[name.lower()]


# Expose common attribute for compatibility
class _DialectsModule:
    @property
    def Snowflake(self):
        _ensure_snowflake_loaded()
        return _dialect_registry["snowflake"]

    def get(self, name: str):
        return get(name)

    def __getitem__(self, name: str):
        return get(name)


dialects = _DialectsModule()

__all__ = ["dialects", "get", "Dialect"]
