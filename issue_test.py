"""Tests for Snowflake and template comment handling."""

import unittest

from sqlglot import TokenType, parse_one, tokenize
import dialects_clean as dialects


class TestSnowflakeComments(unittest.TestCase):
    def test_snowflake_comment_styles_parse(self) -> None:
        base = parse_one("SELECT 1", read=dialects.Snowflake)
        cases = [
            "SELECT 1 -- traditional SQL comment",
            "SELECT 1 /* block comment */",
            "SELECT 1 // C++ style comment",
        ]

        for query in cases:
            with self.subTest(query=query):
                self.assertEqual(parse_one(query, read=dialects.Snowflake), base)

    def test_double_slash_is_comment_in_snowflake(self) -> None:
        tokens = tokenize("SELECT 1 // hi", read=dialects.Snowflake)
        self.assertTrue(
            any(token.type == TokenType.COMMENT and token.text.startswith("//") for token in tokens)
        )
        self.assertFalse(
            any(token.type == TokenType.OPERATOR and token.text == "//" for token in tokens)
        )


class TestTemplateComments(unittest.TestCase):
    def test_template_comment_tokenized_as_single_comment(self) -> None:
        sql = "SELECT 1 {# template -- comment with // and /* */ #}"
        tokens = tokenize(sql, read=dialects.Ansi)
        comment_tokens = [token for token in tokens if token.type == TokenType.COMMENT]

        self.assertEqual(len(comment_tokens), 1)
        self.assertEqual(comment_tokens[0].text, "{# template -- comment with // and /* */ #}")


if __name__ == "__main__":
    unittest.main()
