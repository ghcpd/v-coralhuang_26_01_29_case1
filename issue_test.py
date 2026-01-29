"""Regression tests for comment parsing/tokenization.

Covers:
- Snowflake supports `--`, `/* ... */`, and `//` single-line comments.
- Parsing with and without comments yields equivalent ASTs.
- `//` must not be treated as division.
- Template comments `{# ... #}` are tokenized as a single COMMENT token and
  are handled consistently across dialects.
"""

from __future__ import annotations

import unittest

from sqlglot import dialects, parse_one
from sqlglot.dialects.dialect import Dialect
from sqlglot.expressions import Div
from sqlglot.tokens import TokenType


class TestSnowflakeComments(unittest.TestCase):
    def test_snowflake_comment_styles_parse(self) -> None:
        baseline = parse_one("SELECT 1", read=dialects.Snowflake)

        queries = [
            "SELECT 1 -- traditional SQL comment",
            "SELECT 1 /* block comment */",
            "SELECT 1 // C++ style comment",
            "SELECT 1 /*block*/ --line",
            "SELECT 1 /*block*/ //line",
        ]

        for query in queries:
            with self.subTest(query=query):
                self.assertEqual(parse_one(query, read=dialects.Snowflake), baseline)

    def test_double_slash_is_not_division_in_snowflake(self) -> None:
        ast = parse_one("SELECT 8 // 2", read=dialects.Snowflake)

        # Ensure `//` didn't become two division tokens that build a Div node.
        self.assertFalse(any(isinstance(node, Div) for node in ast.walk()))

        # Semantically equivalent to just `SELECT 8`.
        self.assertEqual(ast, parse_one("SELECT 8", read=dialects.Snowflake))


class TestTemplateComments(unittest.TestCase):
    def test_template_comment_is_single_token_postgres(self) -> None:
        tokenizer = dialects.Postgres.tokenizer()
        tokens = tokenizer.tokenize("SELECT 1 {# hi there #}")

        comment_tokens = [t for t in tokens if t.token_type == TokenType.COMMENT]
        self.assertEqual(len(comment_tokens), 1)
        self.assertEqual(comment_tokens[0].text, "{# hi there #}")

    def test_template_comment_parses_consistently_even_if_comments_overridden(self) -> None:
        class NoLineComments(Dialect):
            LINE_COMMENT_STYLES = ()

        baseline = parse_one("SELECT 1", read=NoLineComments)
        with_comment = parse_one("SELECT 1 {# template #}", read=NoLineComments)
        self.assertEqual(with_comment, baseline)


if __name__ == "__main__":
    unittest.main()
