"""End-to-end test of the entry-point chain without a live Spark session.

Chain: CLI args -> validated settings -> resolved context, mirroring exactly
what ``package_name.main.run`` does before its first Spark call.
"""

from pathlib import Path

from package_name.config import load_settings
from package_name.context import resolve_context
from package_name.utils.cli_parser import parse_args

CONFIG_DIR = Path(__file__).resolve().parents[2] / "src" / "package_name" / "config"


def test_full_context_chain():
    args = parse_args(["--catalog", "main", "--schema", "sales"])
    settings = load_settings(CONFIG_DIR)
    context = resolve_context(args, settings)
    assert context.catalog == "main"
    assert context.schema == "sales"
