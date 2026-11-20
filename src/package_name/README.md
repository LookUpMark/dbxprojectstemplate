# src/sandbox/

Shared Python code, usable by the bundle's jobs and pipelines.

## Contents

- `main.py` — project entry point (the `main` script defined in `pyproject.toml`).
- `utils/` — logging (loguru), CLI parser, common helpers. See `utils/README.md`.

## Conventions

- The package is built as a wheel (`uv build --wheel`) and referenced by the bundle:
  keep the public interface stable.
- Always log with `loguru` (configuration in `utils/logging.py`), never `print`.
- Business logic lives here; files in `tasks/` are just wrappers calling this package.

## Development

```bash
uv sync --dev      # install dependencies
uv run pytest      # tests (in tests/)
task lint          # ruff check + format check
```
