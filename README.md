# Snowflake `//` Comment Parsing Fix (Issue #1763)

## 🔍 Background

Snowflake SQL supports **three** comment forms:

- `--` single-line comments (ANSI-style)
- `/* ... */` block comments
- `//` single-line comments (C/C++-style)

Template-style comments like `{# ... #}` are also used in some templating contexts and should be tokenized as **single, complete comments** across dialects.

## 🐛 What Was Broken (Issue #1763)

Parsing `SELECT 1 // hi this is a comment` with the Snowflake dialect previously failed. The tokenizer did **not** treat `//` as a comment delimiter and instead emitted two `/` tokens. This caused the parser to interpret `//` as division, yielding a syntax error.

**Root cause:** The Snowflake tokenizer's comment configuration lacked the `//` prefix, so the base tokenizer fell back to treating `/` as an operator. Template comments `{# ... #}` could also be split into partial tokens if dialect-specific comment overrides were applied.

## ✅ Fix Summary

- **Snowflake Tokenizer** now explicitly supports `//` single-line comments via `LINE_COMMENT_PREFIXES = ("--", "//")`.
- **Base Tokenizer** always recognizes `{# ... #}` as a template comment, regardless of dialect overrides, ensuring consistent tokenization.
- Block comments `/* ... */` remain supported.
- Comments are tokenized as `COMMENT` tokens and **ignored by the parser**, so they do not affect AST construction.

## 🧪 Test Coverage

Located in `tests/test_comments.py` and `issue_test.py`:

- ✅ Parsing Snowflake queries with `--`, `/* ... */`, and `//` comments succeeds.
- ✅ Queries with and without comments produce **equivalent ASTs**.
- ✅ `//` is **not** parsed as division (tokenized as a single `COMMENT`; no `SLASH` tokens emitted).
- ✅ Template comments `{# ... #}` are tokenized as **one complete `COMMENT` token** using a non-Snowflake dialect (`ansi` alias), preventing partial tokenization regressions.

## 🚀 How to Run Tests (One Command)

Prerequisites:

- Python 3.8+ (3.11 tested)
- `pytest` installed (`pip install pytest` if needed)

Run all tests:

```bash
python run_tests.py
```

Alternative:

```bash
python -m pytest -q
```

## 🔧 Files Touched

- `sqlglot/tokenizer.py` — base tokenizer now recognizes template comments `{# ... #}` globally.
- `sqlglot/dialects/snowflake.py` — Snowflake tokenizer now includes `//` in `LINE_COMMENT_PREFIXES` and retains `/* ... */` block comment support.
- `tests/test_comments.py` — comprehensive comment parsing and tokenization regression tests.
- `issue_test.py` / `minimal_repro.py` — updated to use the local `sqlglot` implementation (no external dependencies).
- `run_tests.py` — one-command test runner.

## 🔒 Regression Prevention

- AST equivalence assertions ensure comments are ignored during parsing.
- Token-level checks guarantee `//` is recognized as a comment delimiter and not emitted as operator tokens.
- Template comment tokenization is covered across dialects to prevent partial parsing when dialect comment rules change.

## 📦 Implementation Notes

This repository contains a **minimal, self-contained** subset of `sqlglot` tailored to demonstrate and fix the comment parsing bug without relying on any pre-installed upstream package. The Snowflake dialect fix lives in `sqlglot/dialects/snowflake.py` and is re-exported via the root `snowflake.py` for compatibility with the provided files.
