# tests/

Unit tests for the shared code in `src/sandbox/`.

## Running

```bash
uv run pytest        # or
task test
```

## Conventions

- One `test_<module>.py` file for each module tested in `src/sandbox/`.
- Sample datasets live in `fixtures/` (no real or sensitive data).
- Use `databricks-connect` only where necessary; prefer pure Python tests
  (fast, runnable locally without a cluster).
- Code in `tasks/` should be structured so the logic lives in the package
  (`src/sandbox/`) and is therefore directly testable.
