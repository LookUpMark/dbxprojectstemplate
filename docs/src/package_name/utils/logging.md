# src/package_name/utils/logging.py

Centralized loguru configuration. One responsibility: format, level, sink.

## Module constant

`_LOG_FORMAT` — single-line message layout:
`HH:mm:ss | LEVEL | module:function - message`. Compact by design, because job
logs are read in the Databricks UI where color and verbosity cost attention.

## Functions

### `configure_logging(level: str = "INFO") -> None`

1. `logger.remove()` — drops every inherited handler so repeated calls (unit
   tests, multiple tasks in one process) never duplicate output.
2. `logger.add(sys.stderr, level=level.upper(), format=_LOG_FORMAT)` — installs
   exactly one sink at the requested level.

Args:
    level: Case-insensitive severity name; `"debug"` becomes `"DEBUG"`.

Conventions:

- Import and call this at the start of every task or job entry point.
- Never `print` in package code; use `logger.info/warning/error`.
