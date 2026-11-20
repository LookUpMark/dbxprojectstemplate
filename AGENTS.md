# Declarative Automation Bundles Project template

This project uses Declarative Automation Bundles (DABs) for deployment on Databricks.

## For AI Agents: Databricks

**Before any other action**: verify the CLI is installed (`databricks --version`,
v1.21.0+). If Databricks AI Tools are not installed for the coding agent:

```bash
databricks aitools install
```

CLI installation: https://docs.databricks.com/dev-tools/cli/install

### Essential commands

| Command | Purpose |
|---------|---------|
| `databricks configure` | Authenticate to the workspace |
| `databricks bundle deploy --target dev` | Development deploy |
| `databricks bundle deploy --target prod` | Production deploy |
| `databricks bundle run <job>` | Run a job/pipeline |
| `uv sync --dev` | Install dependencies |
| `uv run pytest` | Local tests |
| `task --list` | Show available tasks (linting, deploy, run, ...) |

## Project conventions

### Architecture rules (template-wide)

- **Atomic modules**: one responsibility per file; pipelines are chains of pure
  functions; dependencies (Spark session, clients) are injected as parameters.
- **Docstrings**: Google notation, everywhere (package, tasks, notebooks).
- **Comments**: single-line, only for the *why*; no narrative AI-style filler.
- **Commits**: Conventional Commits (Angular notation), e.g. `feat(config): ...`.
- **Configuration**: centralized in `src/package_name/config/` — one YAML per domain
  (`settings.yaml`, `ml.yaml`, `etl.yaml`), one Pydantic model per purpose in
  `config/models.py`, loading/validation only in `config/loader.py`.
- **Tests**: `tests/` mirrors `src/` exactly; unit (no Spark), integration
  (live Databricks Connect), e2e (full chain minus live Spark).
- **Docs**: `docs/` mirrors `src/` — one markdown per file (function-by-function
  walkthrough, in English) plus `docs/overview/` for architecture, pipelines
  and conventions.

### Tasks
- Every `.py` file in `tasks/` must expose a `def task(*) -> None` method.
- Experimentation code is developed as **`.py` Databricks notebook source files**
  (never `.ipynb`) and wrapped in this method so the file can be used as a single
  stage of a Lakeflow job pipeline.

### Notebooks
- Format: `.py` Databricks notebook source files (see `src/notebooks/sample_notebook.py`).
- **Location**: notebooks live in `src/notebooks/` (covered by the `src/` entry in
  `sync.paths`); pipeline-local explorations may also live in `src/<pipeline>/explorations/`.
- **Never `.ipynb`**: do not create or commit Jupyter notebooks.
- First line must be exactly `# Databricks notebook source` (no extra text on it).
- Cells separated by `# COMMAND ----------`; markdown cells use `# MAGIC %md`;
  cell titles use `# DBTITLE 1,<title>`.
- Job parameters arrive via `dbutils.widgets` (e.g. `catalog`, `schema`).
- Never edit anything under `.bundle/` — it is a deploy-managed copy, overwritten
  at every deploy.

### Logging
- Use `loguru` throughout the project. Configuration in `src/package_name/utils/logging.py`.

### CLI parser
- Custom CLI argument parser in `src/package_name/utils/cli_parser.py`.

### Taskfile.yml
- All repetitive commands live in `Taskfile.yml`: ruff (check/fix/format), tests,
  deploy dev/prod, run job, workspace list/download, sync, build, `all`.

### `.agents/` structure
- `.agents/skills/` — operational skills
- `.agents/memory/` — notes and past decisions
- `.agents/instructions/` — task-specific instructions
- `.agents/context/` — project context (config, variables)
- `.agents/checklists/` — deploy and QA checklists

## Deployment

- **Target `dev`** (default): `mode: development`, resources prefixed with `[dev ...`,
  schedules and triggers paused.
- **Target `prod`**: `mode: production`, root path
  `/Workspace/Users/YOUR-EMAIL/.bundle/${bundle.name}/${bundle.target}`.
- Workspace host: `https://YOUR-WORKSPACE-HOST.cloud.databricks.com`

## Project Instructions

<!-- Add project-specific instructions, coding conventions, or notes here -->
