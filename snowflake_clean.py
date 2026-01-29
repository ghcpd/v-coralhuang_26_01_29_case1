from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Dialect:
    SINGLE_LINE_COMMENTS: List[str] = None
    BLOCK_COMMENT_DELIMITERS: List[Tuple[str, str]] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "SINGLE_LINE_COMMENTS", self.SINGLE_LINE_COMMENTS or ["--"])
        object.__setattr__(self, "BLOCK_COMMENT_DELIMITERS", self.BLOCK_COMMENT_DELIMITERS or [("/*", "*/")])


class Snowflake(Dialect):
    def __init__(self) -> None:
        super().__init__(SINGLE_LINE_COMMENTS=["--", "//"], BLOCK_COMMENT_DELIMITERS=[("/*", "*/")])
