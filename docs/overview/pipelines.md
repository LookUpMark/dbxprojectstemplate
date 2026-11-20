# Pipelines

End-to-end walkthrough of each pipeline in the template: phases, files and the
methods invoked at every step.

## Pipeline 1 — sample_job (notebook + wheel task)

Purpose: prove the bundle deploys and runs; sets catalog/schema context and
previews a sample table.

| Phase | File | What happens |
|---|---|---|
| 1. Trigger | `resources/sample_job.job.yml` | Periodic trigger (paused in dev); job-level `catalog`/`schema` parameters |
| 2. Notebook task | `src/notebooks/sample_notebook.py` | Reads widgets `catalog`/`schema`, prints runtime info, checks the schema |
| 3. Wheel task | `tasks/` (thin wrapper) → `src/package_name/main.py::main` | `configure_logging()` → `parse_args()` → `run()` |
| 4. Context | `src/package_name/context.py::resolve_context` | CLI args over settings defaults → `JobContext` |
| 5. SQL context | `main.py::run` | `USE CATALOG` / `USE SCHEMA` |
| 6. Data | `src/package_name/sample_data.py::find_all_sample_data` → `show_head` | `spark.read.table(...)` → `show(5)` |

Run it locally:

```bash
databricks bundle deploy --target dev
databricks bundle run sample_job --target dev
```

## Pipeline 2 — sample_pipeline (Lakeflow / DLT)

Purpose: declarative pipeline skeleton; Databricks computes and refreshes the
tables on every update. Replace the sample transformations with your domain logic.

| Phase | File | What happens |
|---|---|---|
| 1. Definition | `resources/sample_pipeline.pipeline.yml` | Serverless pipeline, catalog/schema from bundle vars, editable env |
| 2. Source | `src/sample_pipeline/transformations/sample_trips.py` | DLT table definition (`@dp.table`) reading a sample table |
| 3. Source | `src/sample_pipeline/transformations/sample_zones.py` | Second table definition; DLT manages dependencies |
| 4. Refresh | Databricks runtime | Dependency resolution, incremental refresh, lineage capture |

## Extending with your own pipelines

1. Add a domain module in `src/package_name/` with pure functions (inject the
   Spark session).
2. Add a YAML config file in `src/package_name/config/` + a Pydantic model in
   `config/models.py` + one entry in `config/loader.py::_DOMAIN_FILES`.
3. Add the job or pipeline definition in `resources/*.yml`.
4. Mirror the tests in `tests/unit|integration|e2e/` and the documentation in
   `docs/src/package_name/`.
