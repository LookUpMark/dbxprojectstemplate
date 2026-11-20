"""YAML configuration loader.

Reads one YAML file per domain, validates each through its Pydantic model and
returns the aggregate :class:`Settings`. Pure filesystem work: no Databricks
runtime dependency, fully unit-testable.
"""

from importlib import resources
from pathlib import Path

import yaml

from package_name.config.models import EtlSettings, GeneralSettings, MlSettings, Settings

# Mapping of domain name -> (yaml filename, validating model).
_DOMAIN_FILES: dict[str, tuple[str, type]] = {
    "general": ("settings.yaml", GeneralSettings),
    "ml": ("ml.yaml", MlSettings),
    "etl": ("etl.yaml", EtlSettings),
}


def _load_domain(path: Path, model: type):
    """Load one YAML file and validate it against a Pydantic model.

    Args:
        path: Path to the YAML file.
        model: Pydantic model class validating the file contents.

    Returns:
        An instance of ``model`` built from the YAML mapping.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        TypeError: If the file is not a mapping.
        ValidationError: If the data fails model validation.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise TypeError(f"Configuration file must contain a mapping: {path}")
    return model(**data)


def load_settings(config_dir: Path | None = None) -> Settings:
    """Load and validate all configuration domains.

    Args:
        config_dir: Directory containing the YAML files. Defaults to the
            packaged ``package_name/config`` directory.

    Returns:
        The validated aggregate settings.

    Raises:
        FileNotFoundError: If any domain file is missing.
        TypeError: If any domain file is not a mapping.
    """
    directory = config_dir or Path(str(resources.files("package_name.config")))
    domains = {name: _load_domain(directory / file, model) for name, (file, model) in _DOMAIN_FILES.items()}
    return Settings(**domains)
