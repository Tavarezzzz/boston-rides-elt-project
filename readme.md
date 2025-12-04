+-----------------------------------------------------------------------+
|                       ORQUESTRADOR: APACHE AIRFLOW                    |
|                  (DAG: dags/elt_pipeline.py - @daily)                 |
+-----------------------------------------------------------------------+
        |
        | (Task 1: extract_to_bronze)
        v
+------------------+            +------------------+
|  FONTE KAGGLE    |            |   CAMADA BRONZE  |
| rideshare.csv    | ---------> |   data/bronze/   |
+------------------+            | (Arquivo Bruto)  |
                                +------------------+
                                         |
                                         | (Task 2: bronze_to_silver)
                                         | Script: src/transform_silver.py
                                         | Tecnol: Python + Pandas (UTF-8 Fix)
                                         v
                                +------------------+
                                |   CAMADA SILVER  |
                                |    data/silver/  |
                                | (Dados Limpos)   |
                                +------------------+
                                         |
                                         | (Task 3: silver_to_gold)
                                         | Script: src/transform_gold.py
                                         | Tecnol: Python + DuckDB (SQL)
                                         v
                                +------------------+
                                |    CAMADA GOLD   |
                                |     data/gold/   |
                                | (KPIs de Negócio)|
                                +------------------+
                                         |
                                         | (Validação Final)
                                         | Script: src/analise_final.py
                                         v
                               [ RELATÓRIO FINAL ]
