import duckdb
import os

def mostrar_kpis():
    base_path = os.getcwd()
    gold_dir = os.path.join(base_path, "data", "gold")
    
    # Lista dos arquivos CSV gerados
    arquivos = [
        ("💰 KPI 1: Preço por Km", "kpi_preco_km.csv"),
        ("🗺️ KPI 2: Top 5 Rotas Mais Caras", "kpi_rotas_caras.csv"),
        ("⚡ KPI 3: Impacto da Tarifa Dinâmica", "kpi_surge_impact.csv")
    ]
    
    print("\n" + "="*50)
    print("📊 RELATÓRIO FINAL (Lendo CSVs)")
    print("="*50)

    for titulo, arquivo in arquivos:
        caminho = os.path.join(gold_dir, arquivo).replace('\\', '/')
        print(f"\n{titulo}")
        print("-" * len(titulo))
        
        try:
            # MUDANÇA: read_csv em vez de read_parquet
            query = f"SELECT * FROM read_csv('{caminho}', header=True) LIMIT 5"
            df = duckdb.sql(query).df()
            print(df.to_string(index=False))
        except Exception as e:
            print(f"Ainda não gerado ou erro: {e}")

if __name__ == "__main__":
    mostrar_kpis()