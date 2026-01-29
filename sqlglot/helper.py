from __future__ import annotations

from typing import Any, List, Optional


def seq_get(seq: List[Any], idx: int, default: Optional[Any] = None) -> Optional[Any]:
    try:
        return seq[idx]
    except (IndexError, TypeError):
        return default

__all__ = ["seq_get"]
