# tasks/

Entry point for executable tasks, run as stages of Lakeflow job pipelines.

## Convention

Every `.py` file in this folder must expose a method:

```python
def task(*) -> None:
    ...
```

Experimentation code (developed as `.py` Databricks notebook source files in
`src/`, never `.ipynb`) is wrapped inside `task()` so the file can be referenced
as a single stage of a job in the bundle (`resources/<job>.job.yml`).

## How to add a new task

1. Develop/validate the logic in a notebook (`src/notebooks/` as `.py` Databricks
   notebook source, or `src/*/explorations/`).
2. Create `tasks/<task_name>.py` with the `def task(*) -> None` method.
3. Import shared code from `src/<package>/` (never duplicate logic).
4. Use `loguru` for logging (never `print`).
5. If the task takes parameters, handle them with the CLI parser in
   `src/<package>/utils/cli_parser.py`.
6. Register the task in a job/pipeline resource in `resources/`.
7. Test: `task check`, then deploy with `task deploy-dev` and run with
   `task run-job -- <job_name>`.

## Execution

```bash
databricks bundle run <job_name>
# or
task run-job -- <job_name>
```
