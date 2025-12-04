from airflow import DAG #Pra criaar o pipeline e rodar as tarefas em py
from airflow.operators.python import PythonOperator 
from datetime import datetime, timedelta
import sys #garantir que o Airflow encontre a pasta src e importe os scripts
import os

# Garante que o Airflow encontre a pasta 'src' 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#Importei as 3 funcoes
from src.extract import extract_to_bronze
from src.transform_silver import bronze_to_silver  
from src.transform_gold import silver_to_gold      

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

    
    t1 >> t2 >> t3