"""Unit tests for package_name.config.models validation."""

import pytest
from pydantic import ValidationError

from package_name.config.models import EtlSettings, GeneralSettings, MlSettings


def test_general_settings_accepts_valid_data():
    settings = GeneralSettings(project_name="package_name", catalog="main", schema="default", log_level="DEBUG")
    assert settings.project_name == "package_name"
    assert settings.log_level == "DEBUG"


def test_general_settings_defaults_log_level():
    settings = GeneralSettings(project_name="package_name", catalog="main", schema="default")
    assert settings.log_level == "INFO"


def test_general_settings_rejects_missing_fields():
    with pytest.raises(ValidationError):
        GeneralSettings(project_name="package_name")


def test_ml_settings_validates_all_fields():
    settings = MlSettings(
        experiment_root="exp", agent_experiment="exp/agents", chat_endpoint="chat", registry_schema="ml"
    )
    assert settings.registry_schema == "ml"


def test_etl_settings_rejects_missing_tables():
    with pytest.raises(ValidationError):
        EtlSettings(scratch_schema="scratch", bronze_table="bronze")


def test_etl_settings_full_construction():
    settings = EtlSettings(
        scratch_schema="scratch",
        bronze_table="bronze",
        silver_table="silver",
        gold_table="gold",
        checkpoint_template="/Volumes/{catalog}/{scratch_schema}/checkpoints/{table}",
    )
    assert settings.silver_table == "silver"
