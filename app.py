import streamlit as st
import duckdb
import os
import pandas as pd # Import unificado no topo
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

# 1. Configuração da Página (Estética Modo Claro)
st.set_page_config(page_title="Boston Rides AI", page_icon="🚕", layout="wide")


st.markdown("""
    <style>
    /* Força o fundo branco e texto escuro no app */
    .stApp { background-color: #ffffff !important; color: #31333f !important; }
    
    /* Mantém o botão roxo com texto branco */
    .stButton>button { background-color: #6a0dad !important; color: white !important; border-radius: 8px; }
    
    /* Configura as bordas e foco dos inputs para roxo */
    .stTextInput>div>div>input { border-color: #6a0dad !important; color: #31333f !important; }
    
    /* Garante que os títulos e textos das abas fiquem visíveis no fundo claro */
    h1, h2, h3, p, label, .stTabs [data-baseweb="tab"] { color: #31333f !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização do Backend
load_dotenv()
DB_PATH = "data/gold/boston_rides.duckdb"

@st.cache_resource
def get_db_connection():
    # Garante que as tabelas existam no DuckDB
    conn = duckdb.connect(DB_PATH)
    conn.execute("CREATE OR REPLACE TABLE kpi_rotas_caras AS SELECT * FROM read_csv_auto('data/gold/kpi_rotas_caras.csv')")
    conn.execute("CREATE OR REPLACE TABLE kpi_preco_km AS SELECT * FROM read_csv_auto('data/gold/kpi_preco_km.csv')")
    conn.execute("CREATE OR REPLACE TABLE kpi_surge_impact AS SELECT * FROM read_csv_auto('data/gold/kpi_surge_impact.csv')")
    conn.close()
    # O Cabo (LangChain) domina a conexão com o banco a partir daqui
    return SQLDatabase.from_uri(f"duckdb:///{DB_PATH}", include_tables=['kpi_rotas_caras', 'kpi_preco_km', 'kpi_surge_impact'])

db = get_db_connection()

# 3. Gerenciamento de Memória (Conversational History)
msgs = StreamlitChatMessageHistory(key="chat_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("Sistema operacional. Como posso ajudar com os dados de Boston hoje?")

# 4. Configuração do Agente
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="tool-calling",
    verbose=True
)

# 5. Interface com Abas (Layout Limpo)
st.title("🚖 Boston Rides: AI Data Intelligence")
aba_chat, aba_dados = st.tabs(["💬 Chat com Agente", "📊 Auditoria de Dados"])

with aba_chat:
    st.subheader("Interação em Linguagem Natural")
    
    # Exibe o histórico de mensagens
    for msg in msgs.messages:
        st.chat_message(msg.type).write(msg.content)

    # Input do Usuárioa
    if prompt := st.chat_input("Pergunte algo sobre as rotas ou preços..."):
        st.chat_message("human").write(prompt)
        
        with st.spinner("O Cérebro está processando a query..."):
            try:
                # Injetamos um prefixo de memória para o agente no prompt
                full_prompt = f"""
                Histórico recente da conversa: {msgs.messages[-3:]}
                Nova Pergunta: {prompt}
                
                Regra: Use apenas as tabelas disponíveis. Se a pergunta for sobre o que falamos antes, use o histórico.
                """
                response = agent_executor.invoke({"input": full_prompt})
                answer = response["output"]
                
                st.chat_message("ai").write(answer)
                msgs.add_user_message(prompt)
                msgs.add_ai_message(answer)
            except Exception as e:
                st.error(f"Processing error: {e}")

with aba_dados:
    st.subheader("Gold Layer Visualization")
    
    tabela_selecionada = st.selectbox("Select the table to audit:", ['kpi_rotas_caras', 'kpi_preco_km', 'kpi_surge_impact'])
    
    # ==============================================================
    # O BYPASS SUPREMO: Lemos direto do Data Lake (CSV) e não do Banco!
    # Isso isola o Pandas do SQLAlchemy e resolve 100% dos erros de versão.
    # ==============================================================
    caminho_csv = f"data/gold/{tabela_selecionada}.csv"
    df = pd.read_csv(caminho_csv).head(10)
    st.dataframe(df, use_container_width=True)