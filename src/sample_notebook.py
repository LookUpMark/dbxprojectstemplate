# Databricks notebook source
# Format notes: cells are separated by "# COMMAND ----------", magic lines
# start with "# MAGIC". Reads the job parameters (catalog, schema) set in
# resources/sample_job.job.yml and runs a quick sanity check. Use this as a
# template for parameterized notebooks in the bundle.

# DBTITLE 1,Setup — job parameters
# COMMAND ----------
# MAGIC %md
# MAGIC # Sample notebook (.py format)
# MAGIC
# MAGIC Reads the job-level parameters `catalog` and `schema` (passed by
# MAGIC `sample_job` via `dbutils.widgets`) and prints the runtime environment.
# MAGIC Use this as a template for parameterized notebooks in the bundle.

# COMMAND ----------
# Job parameters arrive as widgets: sample_job defines catalog and schema
# at job level, so this notebook works unchanged on dev and prod targets.
dbutils.widgets.text("catalog", defaultValue="workspace")
dbutils.widgets.text("schema", defaultValue="default")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

# COMMAND ----------
# DBTITLE 1,Environment check
# COMMAND ----------
# Sanity checks: runtime info and that the target schema exists / is defaultable.
import sys

print(f"Runtime: Databricks {spark.version}")
print(f"Python:  {sys.version.split()[0]}")
print(f"Target:  catalog={catalog!r}, schema={schema!r}")

# COMMAND ----------
# DBTITLE 1,Sample query
# COMMAND ----------
# Minimal query to prove connectivity: sample PySpark code, safe to run anywhere.
# Replace with real logic; keep heavy processing in src/sample_pipeline/.
sample_df = spark.range(5).withColumnRenamed("id", "value")
display(sample_df)

# COMMAND ----------
# DBTITLE 1,Log with loguru
# COMMAND ----------
# Project convention: loguru for logging (see AGENTS.md). If the package wheel
# is attached to the cluster (python_wheel_task installs it), import from package_name.
try:
    from loguru import logger

    logger.info(f"Notebook completed for catalog={catalog}, schema={schema}")
except ImportError:
    # Wheel not attached (e.g. running standalone in the workspace): fall back
    print("loguru not available — install the project wheel to enable logging")
