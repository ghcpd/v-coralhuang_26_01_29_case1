from __future__ import annotations
from typing import Any, Sequence, Optional


def seq_get(seq: Sequence[Any], idx: int, default: Optional[Any] = None) -> Any:
    try:
        return seq[idx]
    except Exception:
        return default
