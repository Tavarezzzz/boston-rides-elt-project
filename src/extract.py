import os

def extract_to_bronze():
    # Pega o caminho da pasta onde o projeto está
    base_path = os.getcwd()
    
    # Caminho esperado do arquivo
    file_path = os.path.join(base_path, "data", "bronze", "rideshare_kaggle.csv")
    
    print(f"--- VERIFICANDO CAMADA BRONZE ---")
    
    # Verifica se o arquivo existe
    if os.path.exists(file_path):
        print(f"SUCESSO: Arquivo encontrado em: {file_path}")
        print("A ingestão manual foi confirmada.")
    else:
        # Se não achar(o Airflow vai ficar vermelho)
        raise FileNotFoundError(f"ERRO: O arquivo não está em {file_path}. Verifique se você renomeou e moveu corretamente!")

if __name__ == "__main__":
    extract_to_bronze()