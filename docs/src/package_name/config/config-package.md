# src/package_name/config/ (package)

Centralized project configuration. Public interface is intentionally small:

```python
from package_name.config import load_settings

settings = load_settings()
settings.general.catalog      # str
settings.ml.chat_endpoint     # str
settings.etl.bronze_table     # str
```

## Package layout

| File | Responsibility |
|---|---|
| `settings.yaml` | General domain values (identity, default catalog/schema, log level) |
| `ml.yaml` | ML domain values (experiments, serving endpoint, registry schema) |
| `etl.yaml` | ETL domain values (medallion tables, checkpoint template) |
| `models.py` | One Pydantic model per domain + aggregate `Settings` |
| `loader.py` | Reads the YAML files, validates, returns `Settings` |

## Design rules

- **Separation of concerns**: YAML holds values, `models.py` holds structure
  and validation, `loader.py` holds I/O. Adding a domain means adding one YAML,
  one model and one line in `loader._DOMAIN_FILES`.
- **Fail fast**: missing files raise `FileNotFoundError`; malformed files raise
  `TypeError`; bad values raise Pydantic `ValidationError` at startup, never at
  run time.
- **No runtime dependencies**: the loader uses `importlib.resources`, so it
  works identically inside the deployed wheel and in local tests.

Detailed walkthroughs: [loader.md](loader.md), [models.md](models.md), and the
YAML guides ([settings.md](settings.md), [ml.md](ml.md), [etl.md](etl.md)).
