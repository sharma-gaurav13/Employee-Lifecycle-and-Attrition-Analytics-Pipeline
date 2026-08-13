# Employee-Lifecycle-and-Attrition-Analytics-Pipeline
# Employee Lifecycle and Attrition Analytics Pipeline

## Project Overview
This project provides an end-to-end data engineering solution designed to process, track, and analyze employee records within a Human Resources (HR) context[cite: 1]. By leveraging cloud data integration and a Medallion Architecture (Bronze, Silver, Gold), the pipeline transforms raw, fragmented daily HR snapshots into clean, aggregated metrics to help organizations understand workforce dynamics and predict attrition risks[cite: 1].

## Key Features
* **Automated Data Processing**: Uses Python to generate daily mock employee snapshots[cite: 1].
* **Medallion Architecture**:
  * **Bronze**: Stores raw daily incoming snapshots[cite: 1].
  * **Silver**: Implements Slowly Changing Dimensions (SCD Type 2) using Delta Lake to track historical changes (e.g., role updates, salary bumps, status changes)[cite: 1].
  * **Gold**: Provides business-ready metrics, including monthly department headcount and attrition rates[cite: 1].
* **Tech Stack**:
  * **Languages**: Python (for data generation), PySpark (for big data processing), SQL (for transformations)[cite: 1].
  * **Workspace**: Databricks for environment management[cite: 1].
  * **Storage**: Delta Lake for ACID-compliant data management[cite: 1].

## Project Structure
```text
hr-attrition-analytics-pipeline/
├── data/               # Directory for generated CSV files
├── source/
│   ├── create_sample_files.py  # Generates initial baseline datasets
│   ├── generate_data.py        # Generates daily batches for pipeline testing
│   └── pipeline.py             # Main PySpark processing pipeline
├── sql/
│   └── gold_transformations.sql # SQL scripts for final business aggregation
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
