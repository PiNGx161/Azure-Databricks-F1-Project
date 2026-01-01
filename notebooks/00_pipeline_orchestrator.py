# Databricks notebook source
# MAGIC %md
# MAGIC # 🏎️ F1 Data Pipeline Orchestrator
# MAGIC ## Master Notebook - Run Complete ETL Pipeline
# MAGIC 
# MAGIC This notebook orchestrates the complete F1 data pipeline execution:
# MAGIC 1. Bronze Layer - Raw Data Ingestion
# MAGIC 2. Silver Layer - Data Transformation
# MAGIC 3. Gold Layer - Business Aggregations
# MAGIC 
# MAGIC **Usage**: Run this notebook to execute the entire pipeline end-to-end.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

import time
from datetime import datetime

# Notebook paths (adjust based on your workspace structure)
NOTEBOOK_BASE_PATH = "/Workspace/Repos/YOUR_PROJECT/F1_Project/notebooks"

notebooks_to_run = [
    ("01_bronze_layer_ingestion", "Bronze Layer - Raw Data Ingestion"),
    ("02_silver_layer_transformation", "Silver Layer - Data Transformation"),
    ("03_gold_layer_aggregations", "Gold Layer - Business Aggregations")
]

# COMMAND ----------

# MAGIC %md
# MAGIC ## Helper Functions

# COMMAND ----------

def run_notebook_with_logging(notebook_name: str, description: str) -> dict:
    """
    Run a notebook and log execution details.
    
    Args:
        notebook_name: Name of the notebook to run
        description: Human-readable description
        
    Returns:
        Dictionary with execution results
    """
    notebook_path = f"{NOTEBOOK_BASE_PATH}/{notebook_name}"
    
    print(f"\n{'='*60}")
    print(f"🚀 Starting: {description}")
    print(f"   Notebook: {notebook_name}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Run the notebook
        result = dbutils.notebook.run(notebook_path, timeout_seconds=3600)
        
        elapsed_time = time.time() - start_time
        
        print(f"\n✅ Completed: {description}")
        print(f"   Duration: {elapsed_time:.2f} seconds")
        
        return {
            "notebook": notebook_name,
            "status": "SUCCESS",
            "duration_seconds": elapsed_time,
            "error": None
        }
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        
        print(f"\n❌ Failed: {description}")
        print(f"   Error: {str(e)}")
        print(f"   Duration: {elapsed_time:.2f} seconds")
        
        return {
            "notebook": notebook_name,
            "status": "FAILED",
            "duration_seconds": elapsed_time,
            "error": str(e)
        }

# COMMAND ----------

# MAGIC %md
# MAGIC ## Execute Pipeline

# COMMAND ----------

# Track execution results
execution_results = []
pipeline_start = time.time()

print("🏁 F1 DATA PIPELINE EXECUTION STARTED")
print(f"   Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   Notebooks to run: {len(notebooks_to_run)}")

# Run each notebook in sequence
for notebook_name, description in notebooks_to_run:
    result = run_notebook_with_logging(notebook_name, description)
    execution_results.append(result)
    
    # Stop pipeline if a notebook fails
    if result["status"] == "FAILED":
        print("\n⚠️ Pipeline stopped due to failure!")
        break

pipeline_duration = time.time() - pipeline_start

# COMMAND ----------

# MAGIC %md
# MAGIC ## Execution Summary

# COMMAND ----------

print("\n" + "="*70)
print("📊 PIPELINE EXECUTION SUMMARY")
print("="*70)

# Summary statistics
successful = sum(1 for r in execution_results if r["status"] == "SUCCESS")
failed = sum(1 for r in execution_results if r["status"] == "FAILED")

print(f"\n📈 Statistics:")
print(f"   Total Notebooks: {len(notebooks_to_run)}")
print(f"   Successful: {successful}")
print(f"   Failed: {failed}")
print(f"   Total Duration: {pipeline_duration:.2f} seconds ({pipeline_duration/60:.2f} minutes)")

print(f"\n📋 Detailed Results:")
print("-"*70)

for result in execution_results:
    status_icon = "✅" if result["status"] == "SUCCESS" else "❌"
    print(f"   {status_icon} {result['notebook']}")
    print(f"      Status: {result['status']}")
    print(f"      Duration: {result['duration_seconds']:.2f} seconds")
    if result["error"]:
        print(f"      Error: {result['error'][:100]}...")
    print()

print("="*70)

if failed == 0:
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
else:
    print("⚠️ PIPELINE COMPLETED WITH ERRORS")
    
print("="*70)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Quality Check

# COMMAND ----------

# Final data quality check - verify tables exist and have data
print("\n📊 DATA QUALITY CHECK")
print("="*60)

databases = ["f1_bronze", "f1_silver", "f1_gold"]

for db in databases:
    try:
        tables = spark.sql(f"SHOW TABLES IN {db}").collect()
        print(f"\n🗄️ Database: {db}")
        print("-"*40)
        
        total_records = 0
        for table in tables:
            table_name = table.tableName
            count = spark.table(f"{db}.{table_name}").count()
            total_records += count
            print(f"   {table_name}: {count:,} records")
        
        print(f"   {'─'*30}")
        print(f"   Total: {total_records:,} records")
        
    except Exception as e:
        print(f"   ⚠️ Error accessing {db}: {str(e)}")

print("\n" + "="*60)
print("✅ DATA QUALITY CHECK COMPLETE")
print("="*60)
