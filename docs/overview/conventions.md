# Conventions

Rules every contributor (and agent) must follow in this template.

## Code structure

- Single atomic modules: one responsibility per file, one purpose per function.
- Function chaining: pipelines are compositions of pure functions; dependencies
  (Spark session, clients) are injected as parameters, never imported at module
  level inside business logic.
- `tasks/*.py` are thin wrappers exposing `def task(*) -> None`; all logic lives
  in `src/package_name/`.
- Experimentation lives in notebooks; validated logic is promoted to the package.

## Documentation

- Docstrings: **Google notation**, everywhere (package, tasks, notebooks).
- Single-line comments: only for the *why*, never restating the code; no
  narrative filler ("Now we...", "This function does...").
- `docs/` mirrors `src/`: one markdown per file, function-by-function
  walkthroughs, plus `docs/overview/` for architecture and pipelines.
- Docs and code comments in English.

## Configuration

- One YAML file per domain in `src/package_name/config/`; one Pydantic model per
  purpose in `config/models.py`; loading and validation only in
  `config/loader.py`.
- No hardcoded configuration values in business code: import `load_settings()`.

## Testing

- `tests/` mirrors `src/` exactly; a module's test is always at the mirrored path.
- Unit tests must not require Spark, network or Databricks auth; integration and
  e2e tests may.
- `uv run pytest tests/unit tests/e2e` must pass without a live workspace.

## Git and automation

- Conventional Commits (Angular notation): `feat`, `fix`, `refactor`, `docs`,
  `test`, `chore` with an optional scope, e.g. `feat(config): ...`.
- Commits authored only by the repository owner; no AI co-author trailers; push
  only on request.
- Repetitive commands live in `Taskfile.yml`; linting gate is
  `task ruff-check` / `task ruff-form`, tests via `uv run pytest`.

## Notebooks

- `.py` Databricks notebook source only, never `.ipynb` (first line
  `# Databricks notebook source`, cells via `# COMMAND ----------`).
- Job parameters arrive via `dbutils.widgets` (`catalog`, `schema`), so the same
  notebook runs on dev and prod unchanged.
