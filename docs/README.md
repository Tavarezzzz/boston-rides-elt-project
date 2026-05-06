# ELT Data Pipeline - Uber & Lyft Analytics

This project implements an end-to-end Data Engineering pipeline (ELT) following the Medallion Architecture (Bronze, Silver, Gold).

## 🗂️ Data Layers:
- **Bronze** (Raw): Stores the raw data (`rideshare.csv`) exactly as ingested from the source.
- **Silver** (Clean): A Python script (`transform_silver.py`) uses Pandas to handle encoding inconsistencies (UTF-16/UTF-8), drop null values, and enforce proper data typing.
- **Gold** (Analytics): A Python script (`transform_gold.py`) leverages DuckDB to execute high-performance analytical SQL, generating the final business KPIs.

## 🎯 About the Project
The goal of this project is to analyze ride-sharing data in Boston to answer key business questions such as:
- Which service is cheaper per km (Uber or Lyft)?
- What are the most expensive routes?
- What is the impact of surge pricing on the final fare?

## 🛠️ Tech Stack
- **Python**: Core programming language.
- **DuckDB**: Analytical processing engine for high-speed SQL queries.
- **Pandas**: Robust handling and ingestion of raw files.
- **Apache Airflow**: Task orchestration (DAG code included).

## 📂 Folder Structure
- `dags/`: Contains the Airflow DAG (`elt.py`).
- `src/`: Extraction and transformation scripts.
- `data/`: Local data storage (Data Lake simulation).

## 🚀 How to Run (Manual Simulation)
1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   
## 🏗 Pipeline Architecture

The data flow follows the **Medallion Architecture** standard (Bronze, Silver, Gold), ensuring governance and quality at every stage.
```mermaid

graph TD
    A[Source: Kaggle CSV] -->|Ingestion| B(Bronze: Raw Data)
    B -->|Data Cleaning via Pandas| C(Silver: Clean Data)
    C -->|Aggregation via DuckDB| D(Gold: Business KPIs)
