# Snowflake `//` comments + template comments `{# ... #}`

This repo contains a minimal local SQL tokenizer/parser (under `sqlglot/`) and a minimal Snowflake dialect (`snowflake.py`) used to reproduce and fix issue #1763:

- In **Snowflake SQL**, `//` is a valid **single-line comment** delimiter:

  ```sql
  SELECT 1 // hi this is a comment
  ```

- Previously, the tokenizer treated `//` as two `/` tokens (division operators). That makes the parser think an expression continues after `SELECT 1`, which fails because it expects a right-hand operand.

## Intended behavior

### Snowflake comment styles

The Snowflake dialect must recognize these comment styles:

- `-- ...` single-line comment
- `/* ... */` block comment
- `// ...` single-line comment (Snowflake-specific)

Comments must be ignored during parsing so they **do not affect AST construction** and are **not misinterpreted as operators**.

### Template comments `{# ... #}`

SQL strings may also contain template-style comments like `{# ... #}`.

These must be recognized as **a single complete comment token** during tokenization:

- They must not be split into partial tokens like `{`, `#`, etc.
- They must be treated consistently across dialects, even if a dialect overrides its normal SQL comment rules.

In this repo, template comments are handled in the tokenizer before any dialect-specific comment markers and before normal symbol/operator parsing.

## Running the tests

From the repository root:

```bash
python -m unittest -v
```

Or use the one-command runner script:

**Prerequisites**

- Python 3.11+ available on PATH as `python`

**Command**

```bash
python run_tests.py
```

## What the tests cover

See `issue_test.py` (loaded by `test_comments.py` for unittest discovery):

- Snowflake parsing for `--`, `/* ... */`, and `//` comments.
- AST equivalence: queries with and without comments produce the same AST.
- Regression that `//` is **not parsed as division** under the Snowflake dialect.
- Template comment tokenization `{# ... #}` as a single COMMENT token using a non-Snowflake dialect (`Postgres`) plus a custom dialect with overridden line-comment rules.
