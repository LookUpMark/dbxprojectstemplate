"""CLI argument parsing for job entry points.

Single responsibility: turn command-line arguments into a typed namespace.
Job parameter definitions stay in the YAML job resources.
"""

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class JobArgs:
    """Parsed job arguments.

    Attributes:
        catalog: Unity Catalog catalog to work in.
        schema: Schema inside ``catalog`` to work in.
    """

    catalog: str
    schema: str


def parse_args(argv: list[str] | None = None) -> JobArgs:
    """Parse job arguments from the command line.

    Args:
        argv: Argument list; defaults to ``sys.argv[1:]`` (standard argparse
            behavior) when omitted, which keeps tests explicit.

    Returns:
        Parsed and validated job arguments.

    Raises:
        SystemExit: If required arguments are missing (argparse behavior).
    """
    parser = argparse.ArgumentParser(description="Databricks job with catalog and schema parameters")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    raw = parser.parse_args(argv)
    return JobArgs(catalog=raw.catalog, schema=raw.schema)
