import pytest

from sqlglot import parse_one, dialects
from sqlglot.tokens import TokenType


@pytest.mark.parametrize(
    "query",
    [
        "SELECT 1 -- traditional SQL comment",
        "SELECT 1 /* block comment */",
        "SELECT 1 // C++ style comment",
    ],
)
def test_snowflake_comments_ignore_ast(query):
    """
    All supported Snowflake comment forms should parse and yield the same AST as a bare SELECT.
    This covers issue #1763 where `//` was previously tokenized as division.
    """

    base = parse_one("SELECT 1", read="snowflake")
    parsed = parse_one(query, read="snowflake")
    assert parsed == base


def test_snowflake_double_slash_not_division_tokens():
    """Tokenization should emit a COMMENT token for //, not two SLASH tokens."""
    toks = dialects()["snowflake"].Tokenizer("SELECT 4 // 2").tokens()
    # Find the first comment token and ensure // is captured
    comment_tokens = [t for t in toks if t.token_type == TokenType.COMMENT]
    assert comment_tokens, "Expected a COMMENT token for //"
    assert comment_tokens[0].text.startswith("//")
    # Ensure no stray SLASH token from the // comment
    slash_tokens = [t for t in toks if t.token_type == TokenType.SLASH]
    assert len(slash_tokens) == 0

    # And parsing should succeed, yielding the same AST as SELECT 4 (not a division)
    assert parse_one("SELECT 4 // 2", read="snowflake") == parse_one("SELECT 4", read="snowflake")


def test_template_comment_tokenization_generic():
    """
    Template comments {# ... #} must be tokenized as a single COMMENT token across dialects.
    This ensures they are not split into partial operators/identifiers when comment rules change.
    """
    sql = "SELECT 1 {# templated comment #}"
    toks = dialects()["ansi"].Tokenizer(sql).tokens()
    # The COMMENT token should include the full {# ... #}
    comments = [t for t in toks if t.token_type == TokenType.COMMENT]
    assert len(comments) == 1
    assert comments[0].text == "{# templated comment #}"


def test_comments_not_affect_ast_equivalence():
    """Queries with and without comments should produce equivalent ASTs."""
    queries = [
        "SELECT 1",
        "SELECT 1 -- trailing",
        "-- leading comment\nSELECT 1",
        "SELECT /* mid */ 1",
        "SELECT 1 // hi",
    ]
    asts = [parse_one(q, read="snowflake") for q in queries]
    assert all(ast == asts[0] for ast in asts), "All ASTs should be equivalent"
