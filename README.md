# Snowflake Comment Parsing Fix

## Summary
Snowflake supports `//` as a single-line comment delimiter in addition to `--` and `/* ... */`. The previous tokenizer treated `//` as a division operator, so parsing `SELECT 1 // comment` failed. This repository now treats `//` as a comment *only* for the Snowflake dialect and ensures template comments like `{# ... #}` are always recognized as complete comments during tokenization.

## Intended behavior
- **Snowflake dialect**: recognizes `--`, `/* ... */`, and `//` as comments.
- **Template comments**: `{# ... #}` are always tokenized as a single comment, independent of dialect overrides.
- **AST stability**: comments do not affect AST construction; parsing with comments should match parsing without comments.

## How to run tests
Prerequisite: Python 3.8+.

Run the test runner script:

- PowerShell:
  - `./run_tests.ps1`
  - If execution policy blocks scripts: `powershell -ExecutionPolicy Bypass -File run_tests.ps1`

## Test coverage
The tests validate:
- Snowflake parsing for all comment styles (`--`, `/* */`, `//`).
- Queries with and without comments produce equivalent ASTs.
- `//` is tokenized as a comment (not an operator) in Snowflake.
- `{# ... #}` is tokenized as a single comment token in a non-Snowflake dialect.

These cases prevent regressions by ensuring comment parsing and tokenization remain dialect-correct and do not interfere with AST construction.
