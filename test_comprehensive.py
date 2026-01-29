"""
Comprehensive test suite for Snowflake comment parsing and template comments
"""

import sys
sys.path.insert(0, 'C:/Bug_Bash/sqlglot/sqlglot')

from sqlglot import parse_one, parse


def test_snowflake_comment_styles():
    """Test that all Snowflake comment styles produce equivalent ASTs"""
    print("=" * 70)
    print("Test 1: Snowflake Comment Styles - AST Equivalence")
    print("=" * 70)
    
    base_query = "SELECT 1"
    queries_with_comments = [
        "SELECT 1 -- comment",
        "SELECT 1 /* comment */",
        "SELECT 1 // comment"
    ]
    
    try:
        base_ast = parse_one(base_query, read='snowflake')
        print(f"Base query: {base_query}")
        print(f"Base AST: {base_ast}")
        print()
        
        all_equivalent = True
        for query in queries_with_comments:
            ast = parse_one(query, read='snowflake')
            # Compare SQL output without comments - remove comments first
            base_sql_no_comments = base_ast.sql(dialect='snowflake', comments=False)
            query_sql_no_comments = ast.sql(dialect='snowflake', comments=False)
            
            is_equivalent = base_sql_no_comments == query_sql_no_comments
            status = "✓" if is_equivalent else "✗"
            print(f"{status} Query: {query}")
            print(f"  Generated SQL (with comments): {ast.sql(dialect='snowflake')}")
            print(f"  Generated SQL (no comments): {query_sql_no_comments}")
            print(f"  Equivalent to base: {is_equivalent}")
            print()
            
            all_equivalent = all_equivalent and is_equivalent
        
        print(f"Result: {'PASSED' if all_equivalent else 'FAILED'}")
        print()
        return all_equivalent
    except Exception as e:
        print(f"✗ FAILED with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_double_slash_not_division():
    """Test that // is not parsed as division operator"""
    print("=" * 70)
    print("Test 2: // is Comment, Not Division")
    print("=" * 70)
    
    try:
        # This should parse as SELECT 1, not as 1 divided by something
        query = "SELECT 1 // this is a comment"
        ast = parse_one(query, read='snowflake')
        
        # Get the expression being selected - should be a single literal
        # Walk the AST to find any Div nodes
        from sqlglot.expressions import Div
        
        has_div_node = False
        for node in ast.walk():
            if isinstance(node, Div):
                has_div_node = True
                break
        
        sql_output = ast.sql(dialect='snowflake')
        
        print(f"Query: {query}")
        print(f"AST: {ast}")
        print(f"Generated SQL: {sql_output}")
        print(f"Contains Div node in AST: {has_div_node}")
        
        # Should NOT contain division node
        success = not has_div_node
        print(f"Result: {'PASSED' if success else 'FAILED'}")
        print()
        return success
    except Exception as e:
        print(f"✗ FAILED with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_template_comments():
    """Test that template comments {# ... #} are handled correctly"""
    print("=" * 70)
    print("Test 3: Template Comments {# ... #}")
    print("=" * 70)
    
    test_cases = [
        ("SELECT 1 {# template comment #}", "snowflake", "Snowflake with template comment"),
        ("SELECT 1 {# comment #} FROM t", "snowflake", "Snowflake with template comment in middle"),
        ("SELECT 1 {# template comment #}", "postgres", "PostgreSQL with template comment"),
        ("SELECT 1 {# template comment #}", "mysql", "MySQL with template comment"),
    ]
    
    all_passed = True
    for query, dialect, description in test_cases:
        try:
            ast = parse_one(query, read=dialect)
            sql_output = ast.sql(dialect=dialect)
            
            # Template comments should be removed/handled
            print(f"✓ {description}")
            print(f"  Query: {query}")
            print(f"  Generated SQL: {sql_output}")
            print()
        except Exception as e:
            print(f"✗ {description}")
            print(f"  Query: {query}")
            print(f"  Error: {e}")
            print()
            all_passed = False
    
    print(f"Result: {'PASSED' if all_passed else 'FAILED'}")
    print()
    return all_passed


def test_multiline_comments():
    """Test multiline comment scenarios"""
    print("=" * 70)
    print("Test 4: Multiline and Complex Comment Scenarios")
    print("=" * 70)
    
    test_cases = [
        ("SELECT 1 /* multi\nline\ncomment */", "snowflake", "Multiline block comment", True),
        ("SELECT 1 // comment\n", "snowflake", "// comment with newline (single statement)", True),
        ("SELECT 1 -- comment\n, 2", "snowflake", "-- comment in select list", True),
        ("SELECT 1; // comment\nSELECT 2", "snowflake", "// comment between statements", True),
    ]
    
    all_passed = True
    for query, dialect, description, expect_success in test_cases:
        try:
            # Try to parse (may return multiple statements)
            result = parse(query, read=dialect)
            if expect_success:
                print(f"✓ {description}")
                print(f"  Query: {repr(query)}")
                print(f"  Parsed statements: {len(result)}")
                for i, stmt in enumerate(result):
                    print(f"  Statement {i+1}: {stmt}")
                print()
            else:
                print(f"✗ {description}")
                print(f"  Query: {repr(query)}")
                print(f"  Expected to fail but succeeded")
                print()
                all_passed = False
        except Exception as e:
            if not expect_success:
                print(f"✓ {description}")
                print(f"  Query: {repr(query)}")
                print(f"  Expected error: {e}")
                print()
            else:
                print(f"✗ {description}")
                print(f"  Query: {repr(query)}")
                print(f"  Error: {e}")
                print()
                all_passed = False
    
    print(f"Result: {'PASSED' if all_passed else 'FAILED'}")
    print()
    return all_passed


def test_comment_edge_cases():
    """Test edge cases for comment parsing"""
    print("=" * 70)
    print("Test 5: Comment Edge Cases")
    print("=" * 70)
    
    test_cases = [
        ("SELECT '//not a comment'", "snowflake", "// inside string literal"),
        ("SELECT '/*not a comment*/'", "snowflake", "/* */ inside string literal"),
        ("SELECT '--not a comment'", "snowflake", "-- inside string literal"),
        ("SELECT 1//", "snowflake", "// at end of query"),
        ("SELECT 1--", "snowflake", "-- at end of query"),
    ]
    
    all_passed = True
    for query, dialect, description in test_cases:
        try:
            ast = parse_one(query, read=dialect)
            sql_output = ast.sql(dialect=dialect)
            print(f"✓ {description}")
            print(f"  Query: {query}")
            print(f"  Generated SQL: {sql_output}")
            print()
        except Exception as e:
            print(f"✗ {description}")
            print(f"  Query: {query}")
            print(f"  Error: {e}")
            print()
            all_passed = False
    
    print(f"Result: {'PASSED' if all_passed else 'FAILED'}")
    print()
    return all_passed


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("COMPREHENSIVE TEST SUITE FOR SNOWFLAKE COMMENTS")
    print("=" * 70 + "\n")
    
    results = []
    results.append(("Comment Styles - AST Equivalence", test_snowflake_comment_styles()))
    results.append(("// is Comment, Not Division", test_double_slash_not_division()))
    results.append(("Template Comments", test_template_comments()))
    results.append(("Multiline Comments", test_multiline_comments()))
    results.append(("Comment Edge Cases", test_comment_edge_cases()))
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} test suites passed")
    print("=" * 70 + "\n")
    
    return all(passed for _, passed in results)


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
