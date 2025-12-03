import duckdb
import os

def silver_to_gold():
    # 1. Configura os caminhos
    base_path = os.getcwd()
    
    # MUDANÇA: Lê .csv da Silver
    raw_input_file = os.path.join(base_path, "data", "silver", "rides_clean.csv")
    raw_output_dir = os.path.join(base_path, "data", "gold")
    
    # Correção de caminhos para Windows
    input_file = raw_input_file.replace('\\', '/')
    output_dir = raw_output_dir.replace('\\', '/')
    
    os.makedirs(raw_output_dir, exist_ok=True)
    
    print("--- INICIANDO CAMADA GOLD (Saída em CSV) ---")
    print(f"Lendo dados da Silver: {input_file}")

    # ---------------------------------------------------------
    # KPI 1: Preço Médio por Km
    # ---------------------------------------------------------
    # MUDANÇA: Extensão .csv
    file_kpi1 = f"{output_dir}/kpi_preco_km.csv"
    
    # MUDANÇA: read_csv no input e FORMAT CSV no output
    query_kpi1 = f"""
        COPY (
            SELECT 
                cab_type,
                ROUND(AVG(price), 2) as preco_medio,
                ROUND(AVG(distance), 2) as distancia_media,
                ROUND(AVG(price) / NULLIF(AVG(distance), 0), 2) as preco_por_km_medio
            FROM read_csv('{input_file}', header=True, auto_detect=True)
            GROUP BY cab_type
        ) TO '{file_kpi1}' (HEADER, DELIMITER ',');
    """
    
    # ---------------------------------------------------------
    # KPI 2: Top 10 Rotas Mais Caras
    # ---------------------------------------------------------
    file_kpi2 = f"{output_dir}/kpi_rotas_caras.csv"
    query_kpi2 = f"""
        COPY (
            SELECT 
                source as origem,
                destination as destino,
                ROUND(AVG(price), 2) as preco_medio,
                COUNT(*) as total_corridas
            FROM read_csv('{input_file}', header=True, auto_detect=True)
            GROUP BY 1, 2
            ORDER BY 3 DESC
            LIMIT 10
        ) TO '{file_kpi2}' (HEADER, DELIMITER ',');
    """

    # ---------------------------------------------------------
    # KPI 3: Impacto da Tarifa Dinâmica
    # ---------------------------------------------------------
    file_kpi3 = f"{output_dir}/kpi_surge_impact.csv"
    query_kpi3 = f"""
        COPY (
            SELECT 
                surge_multiplier,
                COUNT(*) as volume_corridas,
                ROUND(AVG(price), 2) as preco_medio
            FROM read_csv('{input_file}', header=True, auto_detect=True)
            GROUP BY 1
            ORDER BY 1 ASC
        ) TO '{file_kpi3}' (HEADER, DELIMITER ',');
    """

    try:
        duckdb.sql(query_kpi1)
        print(f"KPI 1 salvo em: {file_kpi1}")
        
        duckdb.sql(query_kpi2)
        print(f"KPI 2 salvo em: {file_kpi2}")
        
        duckdb.sql(query_kpi3)
        print(f"KPI 3 salvo em: {file_kpi3}")
        
        print("\nSUCESSO! Pipeline completo gerando CSVs.")
        
    except Exception as e:
        print(f"ERRO NA CAMADA GOLD: {e}")

if __name__ == "__main__":
    silver_to_gold()