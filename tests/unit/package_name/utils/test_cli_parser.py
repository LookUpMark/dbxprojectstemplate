"""Unit tests for package_name.utils.cli_parser."""

from dataclasses import FrozenInstanceError

import pytest

from package_name.utils.cli_parser import JobArgs, parse_args


def test_parse_args_reads_both_flags():
    args = parse_args(["--catalog", "main", "--schema", "sales"])
    assert args == JobArgs(catalog="main", schema="sales")


def test_parse_args_missing_schema_exits():
    with pytest.raises(SystemExit):
        parse_args(["--catalog", "main"])


def test_job_args_is_immutable():
    args = JobArgs(catalog="main", schema="sales")
    with pytest.raises(FrozenInstanceError):
        args.catalog = "other"
