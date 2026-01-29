import sys
from pathlib import Path

# Force using the local sqlglot implementation bundled with the repository
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import sqlglot
from sqlglot import parse_one
from sqlglot.dialects import dialects
from sqlglot.tokens import TokenType


def _ast(sql: str, read="ansi"):
    return parse_one(sql, read=read)


def test_local_sqlglot_is_used():
    # Ensure we are not inadvertently importing a preinstalled sqlglot
    assert str(Path(sqlglot.__file__)).startswith(str(ROOT))


def test_snowflake_comment_styles_equivalent_ast():
    base = _ast("SELECT 1", read="snowflake")
    cases = [
        "SELECT 1 -- traditional SQL comment",
        "SELECT 1 /* block comment */",
        "SELECT 1 // C++ style comment",
        "// leading line comment\nSELECT 1",
        "SELECT 1 -- inline then newline\n",
    ]
    for sql in cases:
        parsed = _ast(sql, read="snowflake")
        assert parsed == base, f"AST should match for: {sql}"


def test_snowflake_double_slash_not_division():
    # In Snowflake, // starts a comment, so parsing should succeed and ignore trailing text
    sql = "SELECT 4 // 2 is ignored"
    parsed = _ast(sql, read="snowflake")
    expected = _ast("SELECT 4", read="snowflake")
    assert parsed == expected

    # Tokenization should yield a COMMENT token for //
    tokenizer = dialects.Snowflake.tokenizer()
    tokens = tokenizer.tokenize(sql)
    # Find the comment token
    comment_tokens = [t for t in tokens if t.token_type == TokenType.COMMENT]
    assert comment_tokens, "Expected a comment token for //"
    assert comment_tokens[0].text.startswith("//")


def test_template_comment_tokenized_as_single_comment_non_snowflake():
    sql = "SELECT {# templated comment #} 1"
    tokenizer = dialects.get("ansi").tokenizer()
    tokens = tokenizer.tokenize(sql)
    # Ensure exactly one COMMENT token representing the whole template comment
    comment_tokens = [t for t in tokens if t.token_type == TokenType.COMMENT]
    assert len(comment_tokens) == 1
    assert comment_tokens[0].text.strip().startswith("{#")
    assert comment_tokens[0].text.strip().endswith("#}")

    # Parsing should ignore the template comment and yield the same AST as without it
    parsed_with_comment = _ast(sql, read="ansi")
    parsed_without_comment = _ast("SELECT 1", read="ansi")
    assert parsed_with_comment == parsed_without_comment


def test_template_comment_not_split_even_when_line_comments_override():
    # Ensure Snowflake override of LINE_COMMENTS does not break template comments
    sql = "SELECT {# still a template comment #} 1 // trailing"
    tokenizer = dialects.Snowflake.tokenizer()
    tokens = tokenizer.tokenize(sql)
    comment_tokens = [t for t in tokens if t.token_type == TokenType.COMMENT]
    # Expect two comments: one template comment and one // line comment
    assert len(comment_tokens) == 2
    assert comment_tokens[0].text.strip().startswith("{#")
    assert comment_tokens[1].text.startswith("//")

    parsed = _ast(sql, read="snowflake")
    expected = _ast("SELECT 1", read="snowflake")
    assert parsed == expected
