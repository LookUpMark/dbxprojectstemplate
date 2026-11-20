# src/package_name/config/loader.py

Loads and validates the YAML configuration. The only module in the package
that touches the filesystem for configuration.

## Module constant

`_DOMAIN_FILES: dict[str, tuple[str, type]]` — maps each domain name to its
YAML filename and the Pydantic model that validates it:

- `general` → `settings.yaml` → `GeneralSettings`
- `ml` → `ml.yaml` → `MlSettings`
- `etl` → `etl.yaml` → `EtlSettings`

Adding a domain requires exactly one entry here (plus the YAML and the model).

## Functions

### `_load_domain(path: Path, model: type)`

Validates one file against one model. Steps:

1. Raises `FileNotFoundError` when `path` does not exist — fail fast, no
   silent defaults.
2. `yaml.safe_load(path.read_text())` parses the file (safe loader: no
   arbitrary object construction).
3. Raises `TypeError` when the result is not a mapping (e.g. the file starts
   with a list), with the offending path in the message.
4. Instantiates `model(**data)`: Pydantic raises `ValidationError` listing
   every bad or missing field, so one run reports all problems at once.

### `load_settings(config_dir: Path | None = None) -> Settings`

Public entry point. Steps:

1. Resolves the directory: the injected `config_dir` if given, otherwise the
   packaged `package_name/config` via `importlib.resources` — identical behavior
   in the wheel and in tests.
2. Iterates `_DOMAIN_FILES` and calls `_load_domain` for each domain.
3. Builds the aggregate `Settings(**domains)`; cross-domain coherence (if any
   rules are added later, e.g. schema name constraints) is validated here by
   the Pydantic aggregate model.
4. Returns the frozen-by-validation `Settings` instance.

## Error contract

| Condition | Exception |
|---|---|
| File missing | `FileNotFoundError` |
| File not a YAML mapping | `TypeError` |
| Field missing/wrong type | `pydantic.ValidationError` |

## Interactions

- Called by: `main.py::run`, tests (`tests/unit/package_name/config/test_loader.py`),
  notebooks that need settings values.
- Calls: `models.py` model classes; no other package imports.
