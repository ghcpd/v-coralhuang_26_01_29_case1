from __future__ import annotations

import typing as t

from sqlglot import tokens as _tokens_mod
from sqlglot import generator as _generator_mod


class Dialect:
    """
    Minimal base Dialect for our trimmed-down sqlglot implementation.
    Dialects can override nested Tokenizer/Parser/Generator classes.

    We avoid importing `sqlglot.parser` at module import time to prevent
    circular import issues. Parser resolution is lazy in `parser()`.
    """

    # Default tokenizer/generator
    class Tokenizer(_tokens_mod.Tokenizer):
        pass

    class Generator(_generator_mod.Generator):
        pass

    @classmethod
    def tokenizer(cls) -> _tokens_mod.Tokenizer:
        return cls.Tokenizer()

    @classmethod
    def parser(cls):  # return type: Parser
        # Lazy import to break circular dependency
        from sqlglot import parser as _parser_mod

        # If the dialect defines a nested Parser, use it; else default
        parser_cls = getattr(cls, "Parser", None)
        if parser_cls is None or parser_cls is Dialect.__dict__.get("Parser"):
            # Default parser
            class _DefaultParser(_parser_mod.Parser):
                pass

            return _DefaultParser()
        return parser_cls()

    @classmethod
    def generator(cls) -> _generator_mod.Generator:
        return cls.Generator()


# Helpers used by snowflake.py ----------------------------------------------

from sqlglot.expressions import Literal  # noqa: E402


def max_or_greatest(*args, **kwargs):  # pragma: no cover - stub
    return None


def min_or_least(*args, **kwargs):  # pragma: no cover - stub
    return None


def rename_func(name: str):  # pragma: no cover - stub
    def _rename(*args, **kwargs):
        return None

    return _rename


def inline_array_sql(*args, **kwargs):  # pragma: no cover - stub
    return None


def var_map_sql(*args, **kwargs):  # pragma: no cover - stub
    return None


def date_trunc_to_time(*args, **kwargs):  # pragma: no cover - stub
    return None


def ts_or_ds_to_date_sql(*args, **kwargs):  # pragma: no cover - stub
    return None


def timestrtotime_sql(*args, **kwargs):  # pragma: no cover - stub
    return None


def timestamptrunc_sql(*args, **kwargs):  # pragma: no cover - stub
    return None


def format_time_lambda(*args, **kwargs):  # pragma: no cover - stub
    # Return a function to mimic upstream API
    def inner(arg_list):
        return None

    return inner


def datestrtodate_sql(*args, **kwargs):  # pragma: no cover - stub
    return None


def date_trunc_to_time(*args, **kwargs):  # pragma: no cover - stub
    return None
