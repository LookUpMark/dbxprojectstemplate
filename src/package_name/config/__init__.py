"""Configuration for the project package.

Public interface::

    from package_name.config import load_settings

    settings = load_settings()
    settings.general.catalog
    settings.ml.chat_endpoint
"""

from package_name.config.loader import load_settings
from package_name.config.models import EtlSettings, GeneralSettings, MlSettings, Settings

__all__ = [
    "EtlSettings",
    "GeneralSettings",
    "MlSettings",
    "Settings",
    "load_settings",
]
