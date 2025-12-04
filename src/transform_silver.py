import pandas as pd
import os

def bronze_to_silver():
    # 1. Configura os caminhos
    base_path = os.getcwd() 
    input_file = os.path.join(base_path, "data", "bronze", "rideshare_kaggle.csv")
    output_dir = os.path.join(base_path, "data", "silver")
    
    # Extensão mudada pra .csv
    output_file = os.path.join(output_dir, "rides_clean.csv")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("--- INICIANDO CAMADA SILVER (Saída em CSV) ---")
    print(f"Lendo arquivo: {input_file}")

    #Leitura
    df = None
    encodings_to_try = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
    
    for encoding in encodings_to_try:
        try:
            df = pd.read_csv(input_file, encoding=encoding)
            print(f"Sucesso ao ler com encoding: {encoding}")
            break 
        except UnicodeDecodeError:
            continue
        except Exception:
            continue

    if df is None:
        raise ValueError("Não foi possível ler o arquivo com nenhuma codificação padrão.")

    try:
        # 3. Transformações
        initial_count = len(df)
        
        # Filtrei os nulos na coluna price
        df = df[df['price'].notna()]
        final_count = len(df)
        
        # Converti timestamp para datetime
        if 'time_stamp' in df.columns:
            df['datetime_clean'] = pd.to_datetime(df['time_stamp'], unit='ms')
        
        print(f"Linhas lidas: {initial_count}")
        print(f"Linhas após limpeza: {final_count}")

        # 4. Salvei em CSV 
        df.to_csv(output_file, index=False) # index=False para remover a col de números 0,1,2... da esquerda
        print(f"SUCESSO! Arquivo salvo em: {output_file}")
        
    except Exception as e:
        print(f"ERRO DURANTE TRANSFORMAÇÃO: {e}")

if __name__ == "__main__":
    bronze_to_silver()