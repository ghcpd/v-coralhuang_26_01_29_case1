# Snowflake `//` comment parsing fix & template comments

## Why this failed before
Snowflake accepts `//` as a single-line comment delimiter, e.g. `SELECT 1 // comment`. The previous tokenizer treated `//` as a division operator and failed to parse the query. Template comments `{# ... #}` could also be split into partial tokens if dialect comment rules were overridden.

## Intended behavior
- **Snowflake comments**: support `--`, `/* ... */`, and `//` as comments.
- **Template comments**: `{# ... #}` are always recognized as a single comment token across dialects.
- **Parser**: comments are ignored for AST construction; queries with comments produce the same AST as the comment-free equivalent.

## Implementation
- Added a minimal local `sqlglot` implementation with dialect support.
- Snowflake tokenizer includes `//` single-line comments.
- Tokenizer prioritizes `{# ... #}` template comments to avoid partial tokenization.

## Tests & coverage
Tests live in `issue_test.py` (pytest):
- Snowflake parses `--`, `/* */`, `//` comments and produces the same AST as `SELECT 1`.
- `//` is not parsed as division (`SELECT 4 // 2` == `SELECT 4`).
- `{# ... #}` comments are tokenized as a single comment in both Snowflake and ANSI dialects.

These tests guard against regressions by asserting AST equivalence and correct tokenization.

## How to run

### One-command test runner (recommended)
Prerequisites:
- Python 3.x (repo provides `.venv`)
- Optional: activate virtualenv `. .\.venv\Scripts\Activate.ps1`
- Script installs `pytest` automatically if missing (requires internet on first run)

Command:
```powershell
powershell -ExecutionPolicy Bypass -File .\run_tests.ps1
```
_Alternatively, from PowerShell with permissive execution policy:_
```powershell
.\run_tests.ps1
```

### Manual
```powershell
. .\.venv\Scripts\Activate.ps1
pip install pytest
pytest -q
python minimal_repro.py
```
