"""
Minimal reproducible code for issue #1763
Issue: Snowflake dialect should support // as a comment delimiter
Query: SELECT 1 // hi this is a comment
Expected: Should parse successfully (works in Snowflake)
Actual: Throws parse error

This test validates the fix by checking that the Snowflake tokenizer
correctly identifies // as a comment delimiter.
"""

from snowflake import Snowflake


def test_snowflake_double_slash_comment():
    """Test that Snowflake dialect can tokenize // comments"""
    query = "SELECT 1 // hi this is a comment"
    
    print(f"Testing query: {query}")
    print(f"Dialect: Snowflake")
    print("-" * 50)
    
    try:
        # Create tokenizer
        dialect = Snowflake()
        tokenizer = dialect.Tokenizer()
        
        # Tokenize the query
        tokens = list(tokenizer.tokenize(query))
        
        # Check that we got some tokens (SELECT, 1)
        # The comment should be stripped out during tokenization
        token_texts = [t.text for t in tokens if t.text.strip()]
        
        print("✓ Tokenization succeeded!")
        print(f"Tokens: {token_texts}")
        
        # Verify the comment was removed (should only have SELECT and 1)
        if 'SELECT' in [t.upper() for t in token_texts] and '1' in token_texts:
            # Verify the comment text is NOT in tokens
            comment_in_tokens = any('hi' in t.lower() or 'comment' in t.lower() 
                                   for t in token_texts)
            if not comment_in_tokens:
                print("✓ Comment was correctly stripped!")
                print("✓ PARSING SUCCEEDED!")
                return True
            else:
                print("✗ Comment text found in tokens (not properly stripped)")
                return False
        else:
            print("✗ Expected tokens not found")
            return False
            
    except Exception as e:
        print("✗ Tokenization failed!")
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_snowflake_double_slash_comment()
    exit(0 if success else 1)
