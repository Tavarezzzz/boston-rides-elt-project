ORQUESTRADOR: Apache Airflow (DAG @daily)
      |
      | (Executa task: extract_to_bronze)
      v
1. FONTE DE DADOS
   Arquivo: rideshare_kaggle.csv
      |
      v
2. CAMADA BRONZE (Data Lake Raw)
   Status: Dado Bruto (Ingestão)
      |
      | (Executa task: transform_to_silver)
      | (Tecnologia: Python + Pandas)
      v
3. CAMADA SILVER (Data Lake Clean)
   Status: Dado Limpo e Padronizado
      |
      | (Executa task: calculate_kpis_gold)
      | (Tecnologia: Python + DuckDB)
      v
4. CAMADA GOLD (Data Mart)
   Status: KPIs de Negócio e Agregações
