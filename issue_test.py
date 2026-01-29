"""
Minimal reproducible code for issue #1763 - BEFORE PR 1765
This demonstrates the issue where Snowflake // comments were not supported

Issue: Snowflake dialect should support // as a comment delimiter
Query: SELECT 1 // hi this is a comment
Expected: Should parse successfully (works in Snowflake)
Actual: Throws parse error (in versions before PR 1765)
"""

from sqlglot import parse_one


def test_snowflake_comments():
    """Test all Snowflake comment styles"""
    
    test_cases = [
        ("SELECT 1 -- traditional SQL comment", "Traditional -- comment"),
        ("SELECT 1 /* block comment */", "Block /* */ comment"),
        ("SELECT 1 // C++ style comment", "C++ style // comment"),
    ]
    
    print("=" * 60)
    print("Testing Snowflake Comment Parsing (Issue #1763)")
    print("=" * 60)
    print()
    
    results = []
    for query, description in test_cases:
        print(f"Test: {description}")
        print(f"Query: {query}")
        print("-" * 60)

        try:
            result = parse_one(query, read='snowflake')
            base = parse_one("SELECT 1", read="snowflake")
            assert result == base, "ASTs should be equivalent when comments are ignored"
            print("✓ PASSED - Parsing succeeded!")
            print(f"  Result: {result}")
            results.append(True)
        except Exception as e:
            print("✗ FAILED - Parsing error!")
            print(f"  Error: {type(e).__name__}: {e}")
            results.append(False)

        print()

    # Summary
    print("=" * 60)
    print(f"Summary: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)

    assert all(results), "One or more Snowflake comment parsing tests failed"


if __name__ == "__main__":
    try:
        test_snowflake_comments()
        exit(0)
    except AssertionError:
        exit(1)
