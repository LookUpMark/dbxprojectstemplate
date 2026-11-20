# Monitoring, secrets and alerting

Operational patterns the template teaches. Everything here is documentation
only — adopt the pieces your project needs.

## Secrets

Secrets are **never** declared in the bundle (they would end up in git).
Databricks stores them in secret scopes; code reads them at runtime.

```python
# Preferred: key-value scope, readable by groups you grant in the UI/CLI
value = dbutils.secrets.get("my-scope", "my-api-key")   # raises if missing

# Scope + key management (CLI, run once by an admin):
databricks secrets create-scope my-scope
databricks secrets put-secret my-scope my-api-key --string-value "..."
```

Conventions:

- Read secrets **only** at the point of use (task or job runtime), never at
  module import time — keeps unit tests secret-free.
- Propagate to dependencies as parameters: the function that needs the key
  receives it as an argument; the module that fetches it stays isolated.
- SQL notebooks and warehouses: `secret(scope, key)` function.

## Job notifications

Declared in the job YAML (see the commented samples at the bottom of
`resources/sample_job.job.yml`):

- `email_notifications.on_failure` — workspace users to email on failure.
- `webhook_notifications` — Slack/Teams/PagerDuty via webhooks configured by
  a workspace admin (job → notifications → webhook id).
- Health: `job_notifications` in the UI can watch consecutive failures.

## Alerting on data

- **SQL alerts** (UI → Alerts): schedule a query and get notified when a
  condition holds (e.g. freshness check `max(ts) < now() - interval 1 DAY`).
  Not bundle-managed; treat as workspace configuration.
- **Pipeline expectations** (Lakeflow): declare data-quality expectations in
  transformations — rows failing `expect` rules are tracked in the pipeline UI:

  ```python
  @dp.table
  @dp.expect_all_or_drop({"valid_id": "id IS NOT NULL", "positive": "amount > 0"})
  def silver_events():
      ...
  ```

## Run health / observability

- Job run results are queryable: `system.lakeflow.job_run_timeline` (system
  schema) for cross-job history in dashboards.
- Each wheel task logs via `configure_logging()` (loguru → stderr) — visible
  in the task run output in the UI.
- MLflow tracing for agents/LLM work: automatic with
  `mlflow.langchain.autolog()` (see the agents assignments if present).

## What the bundle does NOT manage

- Secret scopes and values (by design).
- SQL alerts and dashboards' alert rules (workspace config).
- Cluster policies, instance pools (admin config).

Document these in your project README if your team relies on them.
