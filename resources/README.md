# resources/

Bundle resource configurations: jobs, pipelines, etc.

The `.yml` files here are automatically included by `databricks.yml` via:

```yaml
include:
  - resources/*.yml
```

## How to add a new resource

1. **Job** — create `<name>.job.yml` with a task definition pointing to a file in
   `tasks/` (e.g. `tasks/<task_name>.py` with `def task(*) -> None`).
2. **Pipeline** — create `<name>.pipeline.yml`; pipeline dependencies go in the
   `environment` section of pipeline.yml (they are cached in development, not in
   pyproject).
3. Validate: `task validate` (`databricks bundle validate`).
4. Deploy: `task deploy-dev`, then run with `task run-job -- <name>`.

## Current files

- `sample_job.job.yml` — sample job with a schedule (paused in dev).
- `sample_pipeline.pipeline.yml` — sample ETL pipeline.

See https://docs.databricks.com/dev-tools/bundles/deployment-modes.html for the
dev/prod differences.
