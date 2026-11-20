# src/notebooks/

Experimentation notebooks for the project, referenced by jobs in
`resources/<job>.job.yml` via `notebook_path`.

## ML Engineer playbook

See [the playbook index](#ml-engineer-playbook-assignments) below. Full project
documentation lives in [docs/](../../docs/README.md).

## Format (mandatory)

- **`.py` Databricks notebook source files only — never `.ipynb`**
- First line must be **exactly**: `# Databricks notebook source` (no extra text
  on it, or Databricks will not render the file as a notebook)
- Cells separated by `# COMMAND ----------`
- Markdown cells: `# MAGIC %md` on every line
- Cell titles: `# DBTITLE 1,<title>`

## Conventions

- Job parameters arrive via `dbutils.widgets` (e.g. `catalog`, `schema`), so the
  same notebook works unchanged on dev and prod targets.
- Notebooks sit outside the Python package (`src/sandbox/`): they are synced to
  the workspace (via `sync.paths`) but never included in the built wheel.
- Keep experimentation here; once logic is validated, promote it to the package
  (`src/sandbox/`) or to a task (`tasks/<name>.py` with `def task(*) -> None`).
- Use `loguru` for logging (see `AGENTS.md`).
- Example: `sample_notebook.py` — parameterized template used by `sample_job`.

## ML Engineer playbook (assignments)

Each folder below is a hands-on assignment: README (lesson + exercise + deliverable)
and `databricks_notebook_source.py` (the assignment itself).

| # | Folder | Topic |
|---|---|---|
| 01 | `workspace/` | Workspace & notebooks |
| 02 | `unity-catalog/` | Unity Catalog |
| 03 | `genie/` | AI/BI Genie spaces |
| 04 | `genie-agents/` | Genie as an agent tool |
| 05 | `agents/` | Agent Framework (ChatAgent) |
| 06 | `mlflow-experiments/` | MLflow experiments |
| 07 | `dashboards/` | AI/BI Dashboards |
| 08 | `etl-pipelines/` | Medallion ETL |
| 09 | `lakeflow-jobs/` | Lakeflow Jobs |
| 10 | `cli-mastery/` | CLI mastery |

## Notes

- Never edit files under `.bundle/` — that is a deploy-managed copy, overwritten
  at every deploy. Edit the files here, then `task deploy-dev`.
