# dbxprojectstemplate

Forkable template for production-grade Databricks projects built on
**Declarative Automation Bundles (DABs)**: jobs, pipelines, a testable Python
package, centralized configuration and a documentation wiki — all wired and
ready to deploy.

Read the full documentation in [`docs/README.md`](docs/README.md).

## What is inside

```
databricks.yml          Bundle definition: targets dev/prod, sync paths, variables
resources/*.yml         Jobs and pipelines (declarative, referenced by the CLI)
tasks/                  Thin job-stage wrappers (def task(*) -> None)
src/package_name/       Shared package: business logic, atomic modules
├── config/             YAML-per-domain config + Pydantic models + loader
├── context.py          Pure CLI-args → catalog/schema resolution
├── main.py             Entry point (thin orchestration)
├── sample_data.py      Sample data access (REPLACE with your domain)
└── utils/              Logging (loguru), CLI parser
src/sample_pipeline/    Lakeflow/DLT pipeline skeleton (REPLACE with your logic)
src/notebooks/          Workspace notebooks (.py Databricks notebook source)
tests/                  Mirrors src/: unit (no Spark), integration, e2e
docs/                   Wiki mirroring src/ + architecture/pipelines overviews
scripts/init_template.sh  Post-fork initializer (see below)
.github/workflows/ci.yml  Lint + unit tests on push/PR
Taskfile.yml            Task runner: lint, deploy, run
.agents/                Instructions/context for AI coding agents
```

## Architecture rules baked in

- **Atomic modules**: one responsibility per file; dependencies injected as
  parameters; pipelines are chains of pure functions.
- **Centralized configuration**: one YAML per domain, one Pydantic model per
  purpose, loading only in `config/loader.py`. No hardcoded values in code.
- **Docstrings**: Google notation everywhere; comments explain the *why*.
- **Mirroring**: `tests/` and `docs/` mirror `src/` exactly.
- **Commits**: Conventional Commits (Angular notation).

---

## Post-fork initialization — step by step

Do these once, right after forking or cloning. Everything is mechanical; after
step 5 your project is live on your workspace.

### 0. Prerequisites

- Python 3.12 and [uv](https://docs.astral.sh/uv/) installed.
- [Databricks CLI v2](https://docs.databricks.com/dev-tools/cli/install) (≥ v1.21).
- A Databricks workspace you can access, with a
  [personal access token](https://docs.databricks.com/en/dev-tools/auth/pat.html).
- `gh` (GitHub CLI) only if you forked rather than cloned.

### 1. Install dependencies

```bash
uv sync --dev
```

### 2. Run the initializer

Replaces every placeholder (`dbxprojectstemplate`, `package_name`, `YOUR-EMAIL`)
with your project identity — package directory, imports, tests, docs, configs:

```bash
./scripts/init_template.sh <project-name> <package-name> <email>
# example:
./scripts/init_template.sh sales-forecasting sales_forecasting me@example.com
```

Commit the rename:

```bash
git add -A
git commit -m "chore: initialize project from template"
```

### 3. Point the bundle at your workspace

Search for `TODO(post-fork)` and edit `databricks.yml`:

1. **dev target** → `workspace.host`: your workspace URL (the one printed by
   `databricks configure`).
2. **prod target** → `workspace.host`, `root_path` (`/Workspace/Users/<email>/...`)
   and `permissions.user_name` with the account/service principal that owns prod.
3. Optionally adjust bundle `variables` (catalog/schema defaults per target).

Then authenticate the CLI (one time):

```bash
databricks configure
# verify:
databricks auth env
```

### 4. Validate and deploy

```bash
databricks bundle validate
databricks bundle deploy --target dev     # resources prefixed "[dev <user>]"
databricks bundle run sample_job          # first end-to-end run
```

The job chains: notebook task (reads `catalog`/`schema` widgets) → wheel task
(calls the package entry point). Check the run in **Jobs & Pipelines** in the
workspace UI.

### 5. Replace the samples with your domain

| Sample | Replace with |
|---|---|
| `src/<package>/sample_data.py` | Your data-access module(s); keep functions pure with an injected Spark session |
| `src/sample_pipeline/transformations/` | Your DLT tables/flows |
| `resources/sample_job.job.yml`, `resources/sample_pipeline.pipeline.yml` | Your jobs/pipelines (rename logical keys freely) |
| `src/notebooks/sample_notebook.py` | Your notebooks (`.py` Databricks source only, never `.ipynb`) |
| `src/<package>/config/*.yaml` | Your domains: one YAML + one Pydantic model + one entry in `config/loader.py::_DOMAIN_FILES` |

For every new module, mirror it in `tests/unit/...` (no Spark needed) and in
`docs/src/<package>/...` (one markdown per file, function-by-function).

### 6. Daily loop

```bash
uv run pytest tests/unit tests/e2e   # fast, no workspace needed
uv run pytest                        # full suite (integration needs Databricks auth)
task ruff-check                      # lint gate
task deploy-dev                      # databricks bundle deploy --target dev
task run                             # run the sample job
```

CI (`.github/workflows/ci.yml`) runs ruff + unit tests on every push/PR; keep
it green.

---

## Removing this section

Once your project is initialized, delete everything above the fold and write
your own project description — the template's job is done.
