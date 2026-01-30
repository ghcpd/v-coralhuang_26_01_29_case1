"""
Comprehensive test suite for Snowflake comment parsing (Issue #1763)

This test suite validates that the Snowflake dialect correctly handles all
comment styles and ensures comments don't affect tokenization.

Test coverage:
- Traditional SQL -- comments
- Block /* */ comments  
- C++ style // comments (the main fix for issue #1763)
- Template {# #} comments
- Token equivalence verification
- Multiple comment styles in a single query
"""

from snowflake import Snowflake


def tokenize_query(query, dialect_name='snowflake'):
    """Helper function to tokenize a query"""
    dialect = Snowflake()
    tokenizer = dialect.Tokenizer()
    tokens = list(tokenizer.tokenize(query))
    # Return non-empty token texts
    return [t.text for t in tokens if t.text and t.text.strip()]


def test_snowflake_basic_comments():
    """Test all Snowflake comment styles tokenize successfully"""
    
    test_cases = [
        ("SELECT 1 -- traditional SQL comment", "Traditional -- comment"),
        ("SELECT 1 /* block comment */", "Block /* */ comment"),
        ("SELECT 1 // C++ style comment", "C++ style // comment (issue #1763)"),
        ("SELECT 1 {# template comment #}", "Template {# #} comment"),
    ]
    
    print("=" * 70)
    print("TEST SUITE 1: Basic Comment Parsing")
    print("=" * 70)
    print()
    
    results = []
    for query, description in test_cases:
        print(f"Test: {description}")
        print(f"Query: {query}")
        print("-" * 70)
        
        try:
            tokens = tokenize_query(query)
            print("✓ PASSED - Tokenization succeeded!")
            print(f"  Tokens: {tokens}")
            
            # Check that comment text is not in tokens
            comment_keywords = ['comment', 'traditional', 'block', 'template', 'style']
            has_comment = any(keyword in ' '.join(tokens).lower() for keyword in comment_keywords)
            
            if has_comment:
                print("  ⚠ Warning: Comment text may not be fully stripped")
            
            results.append(True)
        except Exception as e:
            print("✗ FAILED - Tokenization error!")
            print(f"  Error: {type(e).__name__}: {e}")
            results.append(False)
        
        print()
    
    return all(results)


def test_token_equivalence():
    """Test that queries with and without comments produce equivalent token lists"""
    
    print("=" * 70)
    print("TEST SUITE 2: Token Equivalence (Comments Should Not Affect Semantics)")
    print("=" * 70)
    print()
    
    # Test cases: (query_without_comment, query_with_comment, description)
    test_cases = [
        ("SELECT 1", "SELECT 1 -- comment", "-- comment"),
        ("SELECT 1", "SELECT 1 /* comment */", "/* */ comment"),
        ("SELECT 1", "SELECT 1 // comment", "// comment"),
        ("SELECT 1", "SELECT 1 {# comment #}", "{# #} comment"),
        ("SELECT a, b FROM t", "SELECT a, b FROM t -- get data", "-- in FROM clause"),
        ("SELECT a, b FROM t", "SELECT a, b /* cols */ FROM t", "/* */ in middle"),
        ("SELECT a, b FROM t", "SELECT a, b FROM t // end line", "// end line"),
    ]
    
    results = []
    for base_query, commented_query, description in test_cases:
        print(f"Test: Token equivalence with {description}")
        print(f"  Base query: {base_query}")
        print(f"  With comment: {commented_query}")
        print("-" * 70)
        
        try:
            base_tokens = tokenize_query(base_query)
            commented_tokens = tokenize_query(commented_query)
            
            # Compare token lists (ignoring whitespace differences)
            base_normalized = [t.strip() for t in base_tokens if t.strip()]
            commented_normalized = [t.strip() for t in commented_tokens if t.strip()]
            
            if base_normalized == commented_normalized:
                print("✓ PASSED - Token lists are equivalent!")
                print(f"  Tokens: {base_normalized}")
                results.append(True)
            else:
                print("✗ FAILED - Token lists differ!")
                print(f"  Base tokens:      {base_normalized}")
                print(f"  Commented tokens: {commented_normalized}")
                results.append(False)
        except Exception as e:
            print("✗ FAILED - Tokenization error!")
            print(f"  Error: {type(e).__name__}: {e}")
            results.append(False)
        
        print()
    
    return all(results)


def test_double_slash_not_division():
    """Test that // is treated as a comment, not a division operator"""
    
    print("=" * 70)
    print("TEST SUITE 3: Verify // Is Not Treated as Division")
    print("=" * 70)
    print()
    
    results = []
    
    # This should tokenize as "SELECT 1" (with comment), not include division
    query = "SELECT 1 // comment"
    print(f"Test: // should be comment, not division")
    print(f"Query: {query}")
    print("-" * 70)
    
    try:
        tokens = tokenize_query(query)
        token_str = ' '.join(tokens)
        
        # Check that we don't have division operator or extra slashes
        has_division = ('/' in token_str) or ('DIV' in token_str.upper())
        has_select_and_one = 'SELECT' in token_str.upper() and '1' in token_str
        
        if has_select_and_one and not has_division:
            print("✓ PASSED - // correctly treated as comment!")
            print(f"  Tokens: {tokens}")
            results.append(True)
        else:
            print("✗ FAILED - // may have been treated as division!")
            print(f"  Tokens: {tokens}")
            print(f"  Has division: {has_division}")
            results.append(False)
    except Exception as e:
        print("✗ FAILED - Tokenization error!")
        print(f"  Error: {type(e).__name__}: {e}")
        results.append(False)
    
    print()
    return all(results)


def test_multiple_comments():
    """Test queries with multiple comment styles"""
    
    print("=" * 70)
    print("TEST SUITE 4: Multiple Comments in Single Query")
    print("=" * 70)
    print()
    
    test_cases = [
        "SELECT 1 -- first comment\n, 2 // second comment",
        "SELECT /* inline */ 1 // end",
        "SELECT 1 {# template #} -- regular",
    ]
    
    results = []
    for query in test_cases:
        print(f"Test: Multiple comment styles")
        print(f"Query: {repr(query)}")
        print("-" * 70)
        
        try:
            tokens = tokenize_query(query)
            print("✓ PASSED - Tokenization succeeded!")
            print(f"  Tokens: {tokens}")
            results.append(True)
        except Exception as e:
            print("✗ FAILED - Tokenization error!")
            print(f"  Error: {type(e).__name__}: {e}")
            results.append(False)
        
        print()
    
    return all(results)


def test_comment_syntax_validation():
    """Test that the COMMENTS configuration is correctly set"""
    
    print("=" * 70)
    print("TEST SUITE 5: Comment Configuration Validation")
    print("=" * 70)
    print()
    
    dialect = Snowflake()
    tokenizer = dialect.Tokenizer()
    
    print("Test: Verify COMMENTS configuration")
    print("-" * 70)
    
    # Check that tokenizer has COMMENTS attribute
    if not hasattr(tokenizer, 'COMMENTS'):
        print("✗ FAILED - Tokenizer missing COMMENTS attribute")
        return False
    
    comments = tokenizer.COMMENTS
    print(f"COMMENTS configuration: {comments}")
    
    # Check for required comment styles
    required_comments = ['--', '//', ('/*', '*/'), ('{#', '#}')]
    results = []
    
    for comment in required_comments:
        if comment in comments:
            print(f"✓ Found: {comment}")
            results.append(True)
        else:
            print(f"✗ Missing: {comment}")
            results.append(False)
    
    print()
    if all(results):
        print("✓ PASSED - All required comment styles are configured!")
    else:
        print("✗ FAILED - Some comment styles are missing!")
    
    print()
    return all(results)


def main():
    """Run all test suites"""
    print()
    print("=" * 70)
    print("SNOWFLAKE COMMENT PARSING - COMPREHENSIVE TEST SUITE")
    print("Testing fix for Issue #1763: Snowflake // comment support")
    print("=" * 70)
    print()
    
    test_suites = [
        ("Basic Comment Parsing", test_snowflake_basic_comments),
        ("Token Equivalence", test_token_equivalence),
        ("// Not Division", test_double_slash_not_division),
        ("Multiple Comments", test_multiple_comments),
        ("Comment Configuration", test_comment_syntax_validation),
    ]
    
    suite_results = []
    for suite_name, test_func in test_suites:
        try:
            result = test_func()
            suite_results.append((suite_name, result))
        except Exception as e:
            print(f"✗ TEST SUITE '{suite_name}' CRASHED!")
            print(f"  Error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            print()
            suite_results.append((suite_name, False))
    
    # Final summary
    print()
    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    passed = sum(1 for _, result in suite_results if result)
    total = len(suite_results)
    
    for suite_name, result in suite_results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {suite_name}")
    
    print()
    print(f"Overall: {passed}/{total} test suites passed")
    print("=" * 70)
    
    return all(result for _, result in suite_results)


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
