"""
Minimal reproducible code for issue #1763
Issue: Snowflake dialect should support // as a comment delimiter
Query: SELECT 1 // hi this is a comment
Expected: Should parse successfully (works in Snowflake)
Actual: Throws parse error (before fix)
"""

from sqlglot import parse_one


def test_snowflake_double_slash_comment():
    """Test that Snowflake dialect can parse // comments"""
    query = "SELECT 1 // hi this is a comment"
    result = parse_one(query, read="snowflake")
    return result


if __name__ == "__main__":
    try:
        result = test_snowflake_double_slash_comment()
        print(" Parsing succeeded!", result)
    except Exception as e:
        print(" Parsing failed!", e)
        raise
