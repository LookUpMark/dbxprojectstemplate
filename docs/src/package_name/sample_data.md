# src/package_name/sample_data.md

Data-access module for the NYC taxi sample. Atomic functions only: each does
one Spark operation and receives the session as a parameter, so nothing here
imports the Databricks runtime.

## Module constant

`NYC_TRIPS_TABLE = "samples.nyctaxi.trips"` — fully-qualified source table.
Keeping it a named constant means tests and callers reference the same literal.

## Functions

### `read_table(spark: SparkSession, table: str) -> DataFrame`

Generic, single-purpose table reader.

1. Calls `spark.read.table(table)` with the injected session.
2. Returns the DataFrame unchanged — no filtering, no caching, no side effects.

This is the seam that makes the module testable: a test can inject any
session (or a stub returning a fixture DataFrame).

### `find_all_sample_data(spark: SparkSession) -> DataFrame`

Domain-specific convenience over `read_table`.

1. Calls `read_table(spark, NYC_TRIPS_TABLE)`.
2. Returns all trips. Function chaining keeps the generic reader reusable for
   the next domain table without duplication.

### `show_head(df: DataFrame, rows: int = 5) -> None`

Inspection helper, isolated from the readers so data functions stay pure.

1. Calls `df.show(rows)`.
2. Returns `None`; its only effect is printing for interactive/job logs.

## Interactions

- Called by: `main.py::run`.
- Calls: nothing in the package (leaf module).
- Tests: `tests/integration/package_name/test_sample_data.py` exercises
  `find_all_sample_data` against a live Databricks Connect session.
