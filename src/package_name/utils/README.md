# src/sandbox/utils/

Shared package utilities.

## Expected contents

- `logging.py` — centralized **loguru** configuration: format, level,
  sinks (stdout/file). Import it at the start of every task.
- `cli_parser.py` — custom parser for CLI arguments
  (argparse or click). Used by tasks to receive job parameters.
- `helpers.py` — common utilities (dates, paths, I/O, ...).

## Conventions

- One responsibility per module; no business logic here, only tooling.
- Every public function must have type hints and a docstring.
- Modules here must be importable both locally (tests) and on Databricks
  clusters (package wheel).
