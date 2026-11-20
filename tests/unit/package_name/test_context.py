"""Unit tests for package_name.context."""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from package_name.config import load_settings
from package_name.context import JobContext, resolve_context
from package_name.utils.cli_parser import JobArgs

PACKAGED_CONFIG = Path(__file__).resolve().parents[3] / "src" / "package_name" / "config"


def test_resolve_context_prefers_cli_args():
    settings = load_settings(PACKAGED_CONFIG)
    context = resolve_context(JobArgs(catalog="main", schema="sales"), settings)
    assert context == JobContext(catalog="main", schema="sales")


def test_resolve_context_is_frozen():
    settings = load_settings(PACKAGED_CONFIG)
    context = resolve_context(JobArgs(catalog="main", schema="sales"), settings)
    with pytest.raises(FrozenInstanceError):
        context.catalog = "other"
