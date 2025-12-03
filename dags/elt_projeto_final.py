from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# --- IMPORTANTE: Garante que o Airflow encontre a pasta 'src' ---
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- CORREÇÃO DOS IMPORTS (O ERRO ESTAVA AQUI) ---
# O Python precisa saber: "Da pasta SRC, arquivo TAL, importe a FUNÇÃO"
from src.extract import extract_to_bronze
from src.transform_silver import bronze_to_silver  # Nome do arquivo real: transform_silver.py
from src.transform_gold import silver_to_gold      # Nome do arquivo real: transform_gold.py

default_args = {
    'owner': 'roberta_data_engineer',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'elt_uber_lyft_flow',
    default_args=default_args,
    description='Pipeline ELT Completo no Docker',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task 1: Ingestão
    t1 = PythonOperator(
        task_id='extract_raw_data',
        python_callable=extract_to_bronze
    )

    # Task 2: Transformação Silver
    t2 = PythonOperator(
        task_id='transform_to_silver',
        python_callable=bronze_to_silver
    )

    # Task 3: KPIs Gold
    t3 = PythonOperator(
        task_id='calculate_kpis_gold',
        python_callable=silver_to_gold
    )

    # Dependências
    t1 >> t2 >> t3