import pytest

from sqlglot import parse_one, tokenize
from sqlglot.tokens import TokenType


def parse_sf(sql: str):
    return parse_one(sql, read="snowflake")


@pytest.mark.parametrize(
    "query",
    [
        "SELECT 1 -- traditional SQL comment",
        "SELECT 1 /* block comment */",
        "SELECT 1 // C++ style comment",
    ],
)
def test_snowflake_comment_styles_equivalent(query):
    assert parse_sf(query) == parse_sf("SELECT 1")


def test_double_slash_not_division():
    # If // were treated as division, this would misparse; instead it's a comment
    assert parse_sf("SELECT 4 // 2") == parse_sf("SELECT 4")


@pytest.mark.parametrize("dialect", ["ansi", "snowflake"])
def test_template_comment_tokenized_as_single_comment(dialect):
    tokens = tokenize("SELECT {# template #} 1", read=dialect)
    comment_tokens = [t for t in tokens if t.type == TokenType.COMMENT]
    assert len(comment_tokens) == 1
    assert comment_tokens[0].text == "{# template #}"
