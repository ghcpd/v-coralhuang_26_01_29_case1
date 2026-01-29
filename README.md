# Snowflake Comment Parsing Fix

## Overview

This repository contains the fix for issue #1763: **Snowflake dialect should support `//` as a comment delimiter**.

## The Problem

Snowflake SQL supports three types of comment syntax:
1. `--` (standard SQL single-line comments)
2. `/* ... */` (standard SQL block comments)
3. `//` (C++ style single-line comments, Snowflake-specific)

Prior to this fix, the sqlglot parser's Snowflake dialect did not explicitly configure support for `//` comments, which could lead to parsing errors or incorrect interpretation of `//` as a division operator.

Additionally, template-style comments `{# ... #}` (commonly used in Jinja templates) needed to be properly handled during tokenization to ensure they are treated as complete comment blocks rather than being split into partial tokens.

## The Solution

### Changes Made

#### 1. Snowflake Tokenizer Configuration ([snowflake.py](snowflake.py))

Added explicit `COMMENTS` configuration to the `Snowflake.Tokenizer` class:

```python
class Tokenizer(tokens.Tokenizer):
    # ... other configuration ...
    
    # Snowflake supports three comment styles:
    # - Single-line: -- (standard SQL)
    # - Single-line: // (C++ style, Snowflake-specific)
    # - Block: /* */ (standard SQL)
    # - Template: {# #} (Jinja-style template comments)
    COMMENTS = ["--", "//", ("/*", "*/"), ("{#", "#}")]
```

This explicit configuration ensures that:
- The tokenizer recognizes `//` as a comment delimiter, not as a division operator
- All three comment styles are properly tokenized and handled during parsing
- Template comments `{# ... #}` are recognized as single comment tokens
- Comments do not interfere with AST construction

### Why This Fix Works

1. **Explicit Declaration**: By explicitly declaring all supported comment styles in the `COMMENTS` configuration, we ensure the tokenizer correctly identifies comment delimiters before attempting to parse operators.

2. **Tokenization Priority**: Comment tokens are processed during the tokenization phase, before operator parsing, which prevents `//` from being misinterpreted as a division operator.

3. **Dialect-Specific Behavior**: The configuration is specific to the Snowflake dialect, ensuring that Snowflake-specific comment syntax doesn't affect other SQL dialects.

4. **Template Comment Support**: Including `{# #}` comments ensures compatibility with template-based SQL generation tools (like Jinja/dbt), where template comments should be completely removed during tokenization.

## Test Coverage

The fix includes comprehensive test coverage to ensure correctness and prevent regressions:

### Test Files

1. **[minimal_repro.py](minimal_repro.py)**: Minimal reproduction of issue #1763
   - Tests basic `//` comment parsing
   - Verifies the original issue is fixed

2. **[issue_test.py](issue_test.py)**: Basic test for all three Snowflake comment styles
   - Tests `--` comments
   - Tests `/* */` comments
   - Tests `//` comments

3. **[test_comprehensive.py](test_comprehensive.py)**: Comprehensive test suite covering:
   - **AST Equivalence**: Verifies queries with different comment styles produce semantically equivalent ASTs
   - **Division vs Comment**: Ensures `//` is not parsed as a division operator
   - **Template Comments**: Tests `{# ... #}` comment handling across multiple dialects
   - **Multiline Scenarios**: Tests complex comment scenarios including multiline comments
   - **Edge Cases**: Tests comments in string literals, at end of queries, etc.

### Test Scenarios Covered

✅ Parsing Snowflake queries with `--`, `/* */`, and `//` comments  
✅ Verifying queries with and without comments produce equivalent ASTs  
✅ Ensuring `//` is not parsed as a division operator  
✅ Template comments `{# ... #}` tokenized as single, complete comments  
✅ Template comments tested across multiple dialects (Snowflake, PostgreSQL, MySQL)  
✅ Multiline block comments  
✅ Comments at end of queries  
✅ Comments in select lists  
✅ Comments inside string literals (should be preserved)  
✅ Comments between statements  

## Running the Tests

### Prerequisites

- Python 3.7+
- The sqlglot package must be available at `C:/Bug_Bash/sqlglot/sqlglot` (as configured in the test files)
- No external dependencies required beyond the local sqlglot implementation

### Running Individual Tests

```powershell
# Run minimal reproduction test
python minimal_repro.py

# Run basic comment style tests
python issue_test.py

# Run comprehensive test suite
python test_comprehensive.py
```

### Running All Tests (One Command)

Use the provided test runner script:

```powershell
# Run all tests at once (recommended)
python run_tests.py
```

**Note**: The PowerShell script `run_tests.ps1` is also provided, but may encounter Unicode encoding issues in some environments. The Python runner (`run_tests.py`) is the recommended method.

If you want to use the PowerShell script:

```powershell
# Run all tests using PowerShell (may have Unicode issues)
.\run_tests.ps1
```

### Expected Output

All tests should pass with output similar to:

```
✓ PASSED: Comment Styles - AST Equivalence
✓ PASSED: // is Comment, Not Division
✓ PASSED: Template Comments
✓ PASSED: Multiline Comments
✓ PASSED: Comment Edge Cases

Total: 5/5 test suites passed
```

## What the Tests Verify

### 1. Comment Style Equivalence
Ensures that queries with different comment styles produce the same semantic result:
- `SELECT 1` (no comment)
- `SELECT 1 -- comment` (SQL style)
- `SELECT 1 /* comment */` (block style)
- `SELECT 1 // comment` (Snowflake C++ style)

All should produce equivalent ASTs when comments are stripped.

### 2. Division Operator vs Comment
Verifies that `//` in `SELECT 1 // comment` is parsed as a comment, not as:
- `SELECT (1 / /) comment` (division operator)
- `SELECT 1 / / comment` (incomplete expression)

The test walks the AST to ensure no `Div` node exists.

### 3. Template Comment Handling
Ensures `{# ... #}` comments are:
- Recognized as complete comment tokens (not split)
- Handled consistently across dialects
- Not partially parsed as braces and hash symbols

### 4. Complex Scenarios
Tests real-world usage patterns:
- Multiline block comments spanning multiple lines
- Comments at end of statements
- Comments in the middle of SELECT lists
- Comments between statements
- Proper handling of comment delimiters inside string literals

### 5. Regression Prevention
By testing across multiple dialects and scenarios, we ensure:
- The fix doesn't break existing functionality
- Template comments work in non-Snowflake dialects too
- String literals containing comment delimiters are not affected
- All edge cases are covered

## File Structure

```
.
├── snowflake.py              # Snowflake dialect implementation (FIXED)
├── minimal_repro.py          # Minimal reproduction of issue #1763
├── issue_test.py             # Basic test for three comment styles
├── test_comprehensive.py     # Comprehensive test suite
├── run_tests.py              # Python test runner script
├── run_tests.ps1             # PowerShell test runner script
└── README.md                 # This file
```

## Implementation Details

### Comment Token Processing

When the tokenizer encounters potential comment delimiters:

1. **Tokenization Phase**: Comments are identified and tokenized as `COMMENT` tokens
2. **Normalization**: All comment styles are normalized to `/* ... */` format in the output
3. **AST Construction**: Comments are either preserved or stripped based on the `comments` parameter
4. **String Safety**: Comment delimiters inside string literals are properly ignored

### Dialect-Specific Behavior

The `COMMENTS` configuration in the Snowflake tokenizer only affects Snowflake dialect parsing. Other dialects maintain their own comment configurations:

- **Snowflake**: `--`, `//`, `/* */`, `{# #}`
- **PostgreSQL**: `--`, `/* */`, `{# #}` (inherits from base + template)
- **MySQL**: `--`, `#`, `/* */`, `{# #}` (inherits from base + template)
- **Standard SQL**: `--`, `/* */`, `{# #}`

## Contributing

When making changes to comment handling:

1. **Update Tests**: Add test cases to [test_comprehensive.py](test_comprehensive.py)
2. **Test All Scenarios**: Run the complete test suite with `python run_tests.py`
3. **Document Changes**: Update this README with any new comment syntax support
4. **Cross-Dialect Testing**: Ensure changes don't break other dialects

## References

- **Issue #1763**: Snowflake `//` comments not supported
- **PR #1765**: Fix for issue #1763 (this implementation)
- [Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference.html)
- [Snowflake Comment Syntax](https://docs.snowflake.com/en/sql-reference/sql-syntax.html)

## License

This code is part of the sqlglot project. See the main project for license information.
