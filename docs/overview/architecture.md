# Architecture

## What this project is

A forkable Databricks project template built on Declarative Automation Bundles
(DABs). Deploying it creates jobs and pipelines in a Databricks workspace from
code, and the Python package it ships is structured for maximal testability.

## Layers

```
resources/*.yml        Databricks resources: jobs, pipelines (declarative)
tasks/*.py             Task wrappers: def task(*), delegate to the package
src/package_name/           Business logic: atomic modules, pure functions
src/notebooks/         Notebook sources synced to the workspace
src/package_name_etl/       Lakeflow pipeline transformations (databricks-dlt)
tests/                 Mirrors src/: unit, integration, e2e
docs/                  This wiki, mirroring src/ file by file
```

## Request flow (job execution)

1. `resources/sample_job.job.yml` defines the job: trigger, `catalog`/`schema`
   parameters, task DAG.
2. `databricks bundle deploy` uploads everything in `sync.paths` and creates
   the job; `databricks bundle run sample_job` triggers a run.
3. Notebook tasks read parameters via `dbutils.widgets`; wheel tasks call
   `package_name.main:main`, which parses the same parameters.
4. `main` resolves the Unity Catalog context (`package_name.context`) and calls
   data functions (`package_name.sample_data`).

## Configuration flow

YAML per domain (`settings.yaml`, `ml.yaml`, `etl.yaml`) is validated by one
Pydantic model per domain in `config/models.py` and loaded by
`config/loader.py::load_settings`, which returns an aggregate `Settings`.
Everything downstream depends on `Settings`, never on hardcoded literals.

## Testing model

- **Unit**: pure functions with injected dependencies (no Spark).
- **Integration**: chains against a live Databricks Connect session.
- **E2E**: the full entry-point chain minus live Spark calls.

## Extending the template

For a new project: fork, rename the bundle in `databricks.yml`, update
`config/*.yaml` values, replace `sample_data.md` with your domain modules, and keep
the mirroring rules (tests/, docs/) as you add files.
