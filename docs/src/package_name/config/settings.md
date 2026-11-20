# src/package_name/config/settings.yaml (general domain)

Values identifying the project and its default deployment context.

| Key | Model field | Meaning |
|---|---|---|
| `project_name` | `GeneralSettings.project_name` | Logical name for resources and log prefixes |
| `catalog` | `GeneralSettings.catalog` | Default Unity Catalog catalog |
| `schema` | `GeneralSettings.schema` | Default schema inside `catalog` |
| `log_level` | `GeneralSettings.log_level` | Level for `utils.logging.configure_logging` |

Only `log_level` has a default (`INFO`); the other three are required. Edit
these values when forking the template — everything downstream reads them from
the validated model, never from literals.
