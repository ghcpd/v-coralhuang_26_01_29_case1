"""
Minimal reproducible code for issue #1763
Issue: Snowflake dialect should support // as a comment delimiter
Query: SELECT 1 // hi this is a comment
Expected: Should parse successfully (works in Snowflake)
Actual: Throws parse error
"""

import sys
from pathlib import Path
# Ensure we use the local sqlglot implementation bundled with this repo
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sqlglot import parse_one

def test_snowflake_double_slash_comment():
    """Test that Snowflake dialect can parse // comments"""
    query = "SELECT 1 // hi this is a comment"
    
    print(f"Testing query: {query}")
    print(f"Dialect: Snowflake")
    print("-" * 50)
    
    try:
        result = parse_one(query, read='snowflake')
        print("✓ Parsing succeeded!")
        print(f"Result: {result}")
        return True
    except Exception as e:
        print("✗ Parsing failed!")
        print(f"Error: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    success = test_snowflake_double_slash_comment()
    exit(0 if success else 1)
