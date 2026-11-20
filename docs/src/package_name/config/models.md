# src/package_name/config/models.py

Pydantic models: one class per configuration purpose, plus the aggregate.
Pure data definitions — no I/O, no dependencies beyond `pydantic`.

## Models

### `GeneralSettings(BaseModel)`

Project identity and default Databricks context.

- `project_name: str` — used in resource names and log prefixes.
- `catalog: str`, `schema: str` — default Unity Catalog location.
- `log_level: str = Field(default="INFO")` — optional field with a safe
  default; everything else is required, so a truncated YAML fails loudly.

### `MlSettings(BaseModel)`

MLflow and serving configuration.

- `experiment_root: str`, `agent_experiment: str` — workspace experiment paths.
- `chat_endpoint: str` — model serving endpoint for agents.
- `registry_schema: str` — UC schema holding registered models.

### `EtlSettings(BaseModel)`

Medallion pipeline configuration.

- `scratch_schema: str` — schema for the sample medallion tables.
- `bronze_table`, `silver_table`, `gold_table: str` — layer table names.
- `checkpoint_template: str` — path template with `{catalog}`,
  `{scratch_schema}`, `{table}` placeholders, formatted by the caller that
  configures Auto Loader.

### `Settings(BaseModel)`

Aggregate holding one instance of each domain model
(`general`, `ml`, `etl`). Because each field is itself a validated model,
invalid nested values surface during aggregate construction with the domain
path in the error.

## Conventions for extension

- New setting → new typed field in the domain model (required unless a default
  is genuinely safe).
- New domain → new `BaseModel` subclass + entry in `loader._DOMAIN_FILES`.
- Never read YAML directly in business code: always go through `Settings`.
