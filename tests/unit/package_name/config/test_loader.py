"""Unit tests for package_name.config.loader."""

from pathlib import Path

import pytest

from package_name.config import load_settings

# Real packaged configuration files, used by default in these tests.
PACKAGED_DIR = Path(__file__).resolve().parents[4] / "src" / "package_name" / "config"


def test_load_settings_from_packaged_files():
    settings = load_settings(PACKAGED_DIR)
    assert settings.general.project_name == "dbxprojectstemplate"
    assert settings.ml.chat_endpoint
    assert settings.etl.bronze_table == "bronze_events"


def test_load_settings_aggregates_all_domains():
    settings = load_settings(PACKAGED_DIR)
    for domain in (settings.general, settings.ml, settings.etl):
        assert domain is not None


def test_load_settings_missing_dir_raises():
    with pytest.raises(FileNotFoundError):
        load_settings(Path("/nonexistent/config/dir"))


def test_load_settings_invalid_yaml_raises(tmp_path: Path):
    (tmp_path / "settings.yaml").write_text("- not\n- a\n- mapping\n")
    (tmp_path / "ml.yaml").write_text(
        "experiment_root: x\nagent_experiment: y\nchat_endpoint: z\nregistry_schema: ml\n"
    )
    (tmp_path / "etl.yaml").write_text(
        "scratch_schema: s\nbronze_table: b\nsilver_table: si\ngold_table: g\ncheckpoint_template: /tmp/{table}\n"
    )
    with pytest.raises(TypeError):
        load_settings(tmp_path)
