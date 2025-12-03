graph TD
    %% Estilos para ficar Preto e Branco
    classDef bw fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;

    subgraph ORQUESTRACAO [ORQUESTRADOR: AIRFLOW]
        direction TB
        T1(Task 1: Ingestão)
        T2(Task 2: Tratamento Silver)
        T3(Task 3: KPIs Gold)
    end

    SOURCE[FONTE: CSV Kaggle] -->|extract.py| BRONZE[BRONZE: Raw Data]
    BRONZE -->|transform_silver.py / Pandas| SILVER[SILVER: Dados Limpos]
    SILVER -->|transform_gold.py / DuckDB| GOLD[GOLD: KPIs de Negócio]

    %% Aplicando estilo preto e branco
    class SOURCE,BRONZE,SILVER,GOLD bw;
    class T1,T2,T3 bw;
    
    %% Conexão lógica
    T1 -.-> BRONZE
    T2 -.-> SILVER
    T3 -.-> GOLD