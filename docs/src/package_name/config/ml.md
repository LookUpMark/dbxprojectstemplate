# src/package_name/config/ml.yaml (ML domain)

MLflow tracking and model-serving configuration.

| Key | Model field | Meaning |
|---|---|---|
| `experiment_root` | `MlSettings.experiment_root` | Root path for experiments under the user workspace |
| `agent_experiment` | `MlSettings.agent_experiment` | Experiment path for agent development |
| `chat_endpoint` | `MlSettings.chat_endpoint` | Model serving endpoint used by agent notebooks |
| `registry_schema` | `MlSettings.registry_schema` | UC schema holding registered models |

All four fields are required. Your ML notebooks consume these values
consume these values instead of hardcoding endpoints and paths.
