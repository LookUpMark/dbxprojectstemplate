# src/package_name/config/etl.yaml (ETL domain)

Medallion pipeline configuration.

| Key | Model field | Meaning |
|---|---|---|
| `scratch_schema` | `EtlSettings.scratch_schema` | Schema holding the medallion tables |
| `bronze_table` | `EtlSettings.bronze_table` | Raw events table (bronze layer) |
| `silver_table` | `EtlSettings.silver_table` | Cleaned/deduplicated table (silver layer) |
| `gold_table` | `EtlSettings.gold_table` | Customer totals aggregate (gold layer) |
| `checkpoint_template` | `EtlSettings.checkpoint_template` | Auto Loader checkpoint path template |

The template contains `{catalog}`, `{scratch_schema}` and `{table}`
placeholders: the caller formats it (e.g. `format(catalog=..., scratch_schema=...,
table=...)`) when configuring a stream, keeping the loader free of
interpolation logic.
