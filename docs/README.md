# Documentation index

This wiki mirrors the repository: one markdown file per source file, plus
project-level overviews. Read the overviews first, then dive into per-file guides.

## Overviews

- [Architecture](overview/architecture.md) — how the project fits together.
- [Pipelines](overview/pipelines.md) — end-to-end phases, files and methods.
- [Conventions](overview/conventions.md) — the rules this template enforces.
- [Monitoring](overview/monitoring.md) — secrets, job notifications, alerting patterns.

## Source mirror (`src/`)

| Source file | Documentation |
|---|---|
| `src/package_name/main.py` | [main.md](src/package_name/main.md) |
| `src/package_name/sample_data.py` | [sample_data.md](src/package_name/sample_data.md) |
| `src/package_name/context.py` | [context.md](src/package_name/context.md) |
| `src/package_name/config/__init__.py` | [config-package.md](src/package_name/config/config-package.md) |
| `src/package_name/config/loader.py` | [loader.md](src/package_name/config/loader.md) |
| `src/package_name/config/models.py` | [models.md](src/package_name/config/models.md) |
| `src/package_name/config/settings.yaml` | [settings.md](src/package_name/config/settings.md) |
| `src/package_name/config/ml.yaml` | [ml.md](src/package_name/config/ml.md) |
| `src/package_name/config/etl.yaml` | [etl.md](src/package_name/config/etl.md) |
| `src/package_name/utils/logging.py` | [logging.md](src/package_name/utils/logging.md) |
| `src/package_name/utils/cli_parser.py` | [cli_parser.md](src/package_name/utils/cli_parser.md) |

## Tests mirror (`tests/`)

- `tests/unit/` mirrors `src/package_name/` one-to-one: a `test_<file>.py` for
  every module, no Spark or network dependencies.
- `tests/integration/` exercises function chains against a live Databricks
  connection (fixtures in `tests/integration/conftest.py`).
- `tests/e2e/` runs the full entry-point chain minus the live Spark calls.
