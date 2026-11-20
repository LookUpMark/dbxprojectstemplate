# src/package_name/context.py

Resolves the effective Unity Catalog context for a run. Pure module: no
runtime imports, trivially unit-testable.

## Dataclass

`JobContext(frozen=True)` with fields `catalog: str` and `schema: str`.
Frozen by design: once resolved, the context cannot be mutated accidentally by
downstream code — the same immutability guarantee as `JobArgs`.

## Functions

### `resolve_context(args: JobArgs, settings: Settings) -> JobContext`

Single chain step from "what the user asked" to "what the job will use".

1. Reads `args.catalog` and `args.schema` from the parsed CLI arguments.
2. Reads the defaults in `settings.general` (available as fallback values for
   future policies, e.g. "use settings when the argument is empty").
3. Returns a new frozen `JobContext(catalog=args.catalog, schema=args.schema)`.

Today arguments always win; the settings parameter keeps the function
extensible without changing its signature.

## Interactions

- Called by: `main.py::run`.
- Depends on: `JobArgs` (from `utils.cli_parser`), `Settings` (from `config`),
  both as injected values.
- Tests: `tests/unit/package_name/test_context.py` — argument precedence and
  frozenness.
