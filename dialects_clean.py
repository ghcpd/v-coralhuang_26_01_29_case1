from __future__ import annotations

from snowflake_clean import Dialect, Snowflake


class Ansi(Dialect):
    def __init__(self) -> None:
        super().__init__(SINGLE_LINE_COMMENTS=["--"], BLOCK_COMMENT_DELIMITERS=[("/*", "*/")])
