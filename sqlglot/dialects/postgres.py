from __future__ import annotations

from .dialect import Dialect


class Postgres(Dialect):
    """Used for non-Snowflake regression coverage (template comments)."""

    LINE_COMMENT_STYLES = ("--",)
