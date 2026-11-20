# src/package_name/utils/cli_parser.py

CLI argument parsing for job entry points. Single concern: command-line text
in, typed arguments out. Parameter *definitions* stay in the job YAML.

## Dataclass

`JobArgs(frozen=True)` with fields `catalog: str` and `schema: str` — the same
shape job-level parameters use, so notebook tasks and wheel tasks agree on the
contract.

## Functions

### `parse_args(argv: list[str] | None = None) -> JobArgs`

1. Builds an `argparse.ArgumentParser` with description
   `"Databricks job with catalog and schema parameters"`.
2. Adds the two required flags `--catalog` and `--schema` — missing arguments
   make argparse exit with code 2 (`SystemExit`), which callers can rely on.
3. Calls `parser.parse_args(argv)`; passing `None` defers to `sys.argv[1:]`
   (production), while tests pass explicit lists.
4. Wraps the namespace into the frozen `JobArgs(catalog=..., schema=...)` and
   returns it.

The dataclass boundary means the rest of the code never touches argparse —
swapping the parser for click or a widget reader changes only this module.

## Interactions

- Called by: `main.py::main` and `main.py::run` (explicit argument lists).
- Consumed by: `package_name.context.resolve_context`.
- Tests: `tests/unit/package_name/utils/test_cli_parser.py` — happy path, missing
  argument, immutability.
