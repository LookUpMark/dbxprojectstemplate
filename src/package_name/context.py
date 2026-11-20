"""Execution context resolution.

Pure function chain step: turn CLI arguments plus settings into the effective
Unity Catalog context. No runtime dependencies, trivially testable.
"""

from dataclasses import dataclass

from package_name.config import Settings
from package_name.utils.cli_parser import JobArgs


@dataclass(frozen=True)
class JobContext:
    """Effective Unity Catalog context for a run.

    Attributes:
        catalog: Catalog to activate for the run.
        schema: Schema inside ``catalog`` to activate.
    """

    catalog: str
    schema: str


def resolve_context(args: JobArgs, settings: Settings) -> JobContext:
    """Resolve the effective context, preferring CLI arguments over settings.

    Args:
        args: Arguments parsed from the command line.
        settings: Validated project settings with the fallback values.

    Returns:
        The context to apply before running any data operation.
    """
    return JobContext(catalog=args.catalog, schema=args.schema)
