# src/package_name/main.py

Entry point of the Python wheel (`main` script in `pyproject.toml`). Pure
orchestration: parse arguments, resolve context, call data functions.

## Imports

- `databricks.sdk.runtime.spark` — the only place the runtime session is used
  directly in this chain.
- `loguru.logger` — structured logging.
- `package_name.sample_data` — data access functions.
- `package_name.context.resolve_context` — pure context resolution.
- `package_name.config.load_settings` — validated YAML configuration.
- `package_name.utils.cli_parser.parse_args`, `package_name.utils.logging.configure_logging` — tooling.

## Functions

### `run(catalog: str, schema: str) -> None`

The job body, separated from `main` so it is callable from tests and other
tasks. Steps, in order:

1. Builds the argument list and calls `parse_args(["--catalog", catalog, "--schema", schema])`
   to obtain a `JobArgs`.
2. Calls `load_settings()` to get the validated aggregate `Settings`.
3. Calls `resolve_context(args, settings)`, returning the effective
   `JobContext` (arguments win over settings).
4. Executes `USE CATALOG` and `USE SCHEMA` through the runtime `spark` session.
5. Logs the active context at INFO.
6. Calls `sample_data.find_all_sample_data(spark)` and passes the DataFrame to
   `sample_data.show_head`, printing 5 rows.

### `main() -> None`

Console-script entry point:

1. `configure_logging()` — installs the loguru sink at INFO.
2. `parse_args()` — reads `sys.argv` (argparse defaults), requiring `--catalog`
   and `--schema`.
3. `run(catalog=args.catalog, schema=args.schema)` — delegates to the function
   above.

### `if __name__ == "__main__": main()`

Allows `python -m` style direct execution with identical behavior.

## Interactions

- Called by: wheel tasks in job resources, `main` console script.
- Calls: `cli_parser`, `config`, `context`, `sample_data`, `logging`.
- Tests: `tests/e2e/test_entry_context.py` covers the chain up to the context
  resolution; the Spark steps are covered by integration tests.
