"""Job entry point.

Thin orchestration only: parse CLI args, apply catalog/schema context, call
package functions. All logic lives in the imported modules.
"""

from databricks.sdk.runtime import spark
from loguru import logger

from package_name import sample_data
from package_name.config import load_settings
from package_name.context import resolve_context
from package_name.utils.cli_parser import parse_args
from package_name.utils.logging import configure_logging


def run(catalog: str, schema: str) -> None:
    """Set the catalog/schema context and preview the taxi sample table.

    Args:
        catalog: Unity Catalog catalog to activate.
        schema: Schema inside ``catalog`` to activate.
    """
    context = resolve_context(parse_args(["--catalog", catalog, "--schema", schema]), load_settings())
    spark.sql(f"USE CATALOG `{context.catalog}`")
    spark.sql(f"USE SCHEMA `{context.schema}`")
    logger.info(f"Context set: catalog={context.catalog}, schema={context.schema}")

    sample_data.show_head(sample_data.find_all_sample_data(spark))


def main() -> None:
    """Entry point wired in ``pyproject.toml`` as the ``main`` script."""
    configure_logging()
    args = parse_args()
    run(catalog=args.catalog, schema=args.schema)


if __name__ == "__main__":
    main()
