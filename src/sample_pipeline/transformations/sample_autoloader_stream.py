"""Sample streaming ingestion with Auto Loader (cloudFiles).

Teaching sample for incremental file ingestion in a Lakeflow pipeline.
Ingestion is *incremental and exactly-once*: the pipeline service manages
checkpoints and state automatically, so no manual checkpoint logic is needed
here. Delete this file if your project has no streaming sources.
"""

from pyspark import pipelines as dp

# Landing path where source files arrive (JSON here; cloudFiles also supports
# csv, parquet, delta, avro...). In a real project this points to the
# landing volume declared in resources/schema.yml, e.g.:
#   /Volumes/{catalog}/{schema}/landing
LANDING_PATH = "/Volumes/workspace/default/landing"

# Format hint for Auto Loader's schema inference and evolution.
FILE_FORMAT = "json"


@dp.table(
    comment="Raw landing data ingested incrementally with Auto Loader (bronze).",
)
def sample_landing_bronze():
    """Incrementally ingest every new file from the landing path.

    Key Auto Loader options demonstrated:
      - cloudFiles.format: source file format.
      - cloudFiles.schemaLocation: where the inferred schema is kept
        (required for schema evolution; a stable path per source).
      - cloudFiles.schemaEvolutionMode: addNewColumns lets new fields in
        incoming files extend the schema instead of failing the stream.
    """
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", FILE_FORMAT)
        .option("cloudFiles.schemaLocation", f"{LANDING_PATH}/_schema")
        .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
        .load(LANDING_PATH)
    )
