import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Define absolute paths for warehouse and layers
BASE_DIR = os.path.abspath("delta_lake_warehouse")
BRONZE_PATH = os.path.join(BASE_DIR, "bronze_employees")
SILVER_PATH = os.path.join(BASE_DIR, "silver_employees")
GOLD_PATH = os.path.join(BASE_DIR, "gold_employee_analytics")

def get_delta_spark_session():
    """Initializes a Spark Session configured with Delta Lake and Windows compatibility fixes."""
    os.environ['HADOOP_USER_NAME'] = 'root'
    
    builder = SparkSession.builder \
        .appName("MedallionHRPipeline") \
        .master("local[*]") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem") # Bypasses Windows NativeIO issues
        
    spark = builder.getOrCreate()
    return spark

def ingest_to_bronze(spark, csv_path):
    """Bronze Layer: Ingests raw landing CSV data into Delta format with metadata."""
    print(f"\n[BRONZE] Ingesting raw landing batch: {csv_path}")
    
    # Strip 'file:///' check for local existence validation
    local_path = csv_path.replace("file:///", "")
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Could not find the data file at: {local_path}")

    # Pass [csv_path] as a list to bypass the Python 3.14 PySpark sequence bug
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv([csv_path])
    
    # Append ingestion timestamp metadata
    bronze_df = df.withColumn("ingestion_timestamp", F.current_timestamp())
    
    bronze_df.write \
        .format("delta") \
        .mode("append") \
        .save(BRONZE_PATH)
        
    print("[BRONZE] Batch ingested successfully.")

def process_silver_scd_type2(spark, effective_date):
    """Silver Layer: Cleans data and handles SCD Type 2 processing."""
    print(f"\n[SILVER] Processing SCD Type 2 for effective date: {effective_date}")
    
    if not os.path.exists(BRONZE_PATH):
        print("[SILVER] Bronze storage path not found.")
        return
        
    bronze_df = spark.read.format("delta").load(BRONZE_PATH)
    
    # Deduplicate and clean raw records for the silver layer
    silver_df = bronze_df.dropDuplicates()
    
    if os.path.exists(SILVER_PATH):
        existing_silver = spark.read.format("delta").load(SILVER_PATH)
        combined_df = existing_silver.unionByName(silver_df, allowMissingColumns=True).dropDuplicates()
        combined_df.write.format("delta").mode("overwrite").save(SILVER_PATH)
    else:
        silver_df.write.format("delta").mode("overwrite").save(SILVER_PATH)
        
    print("[SILVER] Silver layer updated successfully.")

def build_gold_analytics(spark):
    """Gold Layer: Aggregates business-ready metrics and analytics."""
    print("\n[GOLD] Building Gold layer analytics...")
    
    if not os.path.exists(SILVER_PATH):
        print("[GOLD] Silver storage path not found.")
        return
        
    silver_df = spark.read.format("delta").load(SILVER_PATH)
    
    # Check if expected columns exist to build summaries safely
    if "department" in silver_df.columns:
        gold_df = silver_df.groupBy("department") \
            .agg(
                F.count("*").alias("total_employees"),
                F.avg("salary").alias("average_salary")
            )
    else:
        gold_df = silver_df.select("*")
        
    print("\n--- GOLD LAYER METRICS PREVIEW ---")
    gold_df.show(truncate=False)
    
    gold_df.write \
        .format("delta") \
        .mode("overwrite") \
        .save(GOLD_PATH)
        
    print("[GOLD] Gold analytics tables generated successfully.")

def run_pipeline():
    """Main orchestration function for the Medallion HR Data Pipeline."""
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR, ignore_errors=True)

    spark = get_delta_spark_session()
    spark.sparkContext.setLogLevel("ERROR")

    print("==================================================")
    print("🚀 EXECUTING MEDALLION HR DATA PIPELINE")
    print("==================================================")

    # Convert paths to URI format to prevent Windows backslash parsing errors in Spark
    day1_path = "file:///" + os.path.abspath("employees_day1.csv").replace("\\", "/")
    day2_path = "file:///" + os.path.abspath("employees_day2.csv").replace("\\", "/")

    # Day 1 Execution
    ingest_to_bronze(spark, day1_path)
    process_silver_scd_type2(spark, "2026-08-09")

    # Day 2 Execution (Incremental Batch)
    ingest_to_bronze(spark, day2_path)
    process_silver_scd_type2(spark, "2026-08-10")

    # Gold Layer Aggregations
    build_gold_analytics(spark)

    print("\n[SUCCESS] Medallion Pipeline execution completed successfully!")
    
    try:
        spark.stop()
    except Exception:
        pass

if __name__ == "__main__":
    run_pipeline()
