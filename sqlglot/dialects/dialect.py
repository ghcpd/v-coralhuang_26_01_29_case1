from __future__ import annotations

import typing as t

from ..tokens import Tokenizer


class Dialect:
    """Minimal dialect with a tokenizer factory."""

    LINE_COMMENT_STYLES: t.Tuple[str, ...] = ("--",)

    @classmethod
    def tokenizer(cls) -> Tokenizer:
        return Tokenizer(line_comment_starts=cls.LINE_COMMENT_STYLES)
