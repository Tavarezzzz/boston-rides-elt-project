# import duckdb
# import os
# from dotenv import load_dotenv
# from langchain_community.utilities import SQLDatabase
# from langchain_groq import ChatGroq
# from langchain_community.agent_toolkits import create_sql_agent

# # 1. Definição de caminhos
# DB_PATH_FISICO = "data/gold/boston_rides.duckdb"
# URI_LANGCHAIN = f"duckdb:///{DB_PATH_FISICO}"

# def inicializar_e_conectar():
#     print("> [ETAPA 1] Materializando CSVs para DuckDB...")
#     conn = duckdb.connect(DB_PATH_FISICO)
    
#     try:
#         # Injeta os dados limpos da camada Gold no banco analítico
#         conn.execute("CREATE OR REPLACE TABLE kpi_rotas_caras AS SELECT * FROM read_csv_auto('data/gold/kpi_rotas_caras.csv')")
#         conn.execute("CREATE OR REPLACE TABLE kpi_preco_km AS SELECT * FROM read_csv_auto('data/gold/kpi_preco_km.csv')")
#         conn.execute("CREATE OR REPLACE TABLE kpi_surge_impact AS SELECT * FROM read_csv_auto('data/gold/kpi_surge_impact.csv')")
#         print("> Tabelas materializadas com sucesso.")
#     except Exception as e:
#         print(f"> [ERRO NA INJEÇÃO]: {e}")
#         return None
#     finally:
#         conn.close()

#     print("> [ETAPA 2] Conectando o 'Cabo' (LangChain)...")
#     try:
#         # A trava de segurança contra o erro de pg_collation do SQLAlchemy
#         tabelas_gold = ['kpi_rotas_caras', 'kpi_preco_km', 'kpi_surge_impact']
#         db = SQLDatabase.from_uri(URI_LANGCHAIN, include_tables=tabelas_gold)
        
#         print(f"> CONEXÃO BEM SUCEDIDA. Tabelas mapeadas: {db.get_usable_table_names()}")
#         return db
#     except Exception as e:
#         print(f"> [ERRO DE CONEXÃO LANGCHAIN]: {e}")
#         return None

# # ==========================================
# # EXECUÇÃO DA ARQUITETURA C.F.C.
# # ==========================================

# # 1. Prepara a Ferramenta (DuckDB) e o Cabo (LangChain)
# meu_banco = inicializar_e_conectar()

# if meu_banco is None:
#     print("\n> [FALHA CRÍTICA] Abortando missão. O banco de dados não está acessível.")
#     exit()

# # 2. Carrega as variáveis de ambiente do arquivo .env invisível
# load_dotenv()

# # Validação de segurança: Garante que a chave existe antes de chamar a IA
# if not os.getenv("GROQ_API_KEY"):
#     print("\n> [ALERTA DE SEGURANÇA] Chave GROQ_API_KEY não encontrada no arquivo .env!")
#     exit()

# print("\n> [ETAPA 3] Acordando o 'Cérebro' (Llama 3.3 via Groq)...")
# try:
#     # Instancia o LLM com temperatura 0 para respostas determinísticas
#     llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    
#     print("> [ETAPA 4] Fundindo C.F.C. e instanciando o Agente...")
#     # Criamos o Agente passando o Cérebro (llm) e a Ferramenta (meu_banco)
#     estagiario = create_sql_agent(
#         llm=llm,
#         db=meu_banco,
#         agent_type="tool-calling", 
#         verbose=True # Mantém o log de pensamento ativado para debugarmos os erros depois
#     )
    
#     print("> AGENTE PRONTO PARA OPERAÇÃO.\n")
#     print("====================================================")
    
#     # O Teste de Fogo
#     pergunta_diretoria = """
#     Você é um Engenheiro de Dados Sênior. Siga estas REGRAS OBRIGATÓRIAS:
#     1. Você DEVE usar APENAS as tabelas fornecidas pelo banco de dados.
#     2. NUNCA invente nomes de tabelas (como 'prices', 'listings' ou 'rides').
#     3. SEMPRE inspecione o schema das tabelas disponíveis (kpi_preco_km, kpi_rotas_caras, kpi_surge_impact) antes de escrever a query SQL.
#     4. Baseado no schema correto, responda à pergunta abaixo.

#     Pergunta do Usuário: Quais são os 3 destinos mais caros partindo do Financial District? Traga apenas os nomes dos destinos e os preços médios.
#     """
    
#     print(f"> INQUÉRITO DO USUÁRIO: '{pergunta_diretoria}'\n")
    
#     # O Agente assume o controle aqui e faz o raciocínio via LangChain
#     resultado = estagiario.invoke({"input": pergunta_diretoria})
    
#     print("\n====================================================")
#     print(f"> RESPOSTA FINAL ENTREGUE AO USUÁRIO:\n{resultado['output']}")

# except Exception as e:
#     print(f"> [ERRO NO SISTEMA NERVOSO]: Falha na execução do Agente: {e}")