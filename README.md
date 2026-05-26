# 🚖 Boston Rides: AI Data Intelligence & ELT Pipeline

An enterprise-grade Data Lakehouse and AI-powered analytical platform designed to process, orchestrate, and query urban mobility data using Natural Language.

This project bridges the gap between complex data infrastructure and business accessibility by combining a robust ELT pipeline (Medallion Architecture) with a secure, autonomous Text-to-SQL Artificial Intelligence Agent.

---

## 🏗️ System Architecture

The architecture is divided into two main modules: **Data Engineering** (Backend/ELT) and **Artificial Intelligence** (Frontend/Consumption).

### 1. ELT Data Pipeline (Medallion Architecture)
Orchestrated via **Apache Airflow**, raw ride-sharing data flows through three distinct layers processed by **DuckDB** for high-performance, in-memory analytical transformations:

* **Bronze Layer:** Ingestion of raw CSV files (Uber & Lyft metrics).
* **Silver Layer:** Data cleaning, type casting, and schema standardization.
* **Gold Layer:** Business-level aggregations (KPIs for pricing, surge impact, and expensive routes) exported for downstream consumption.

### 2. Autonomous AI Agent (Text-to-SQL)
A consumption layer built with **Streamlit** and **LangChain**, utilizing Meta's **Llama 3.3** model to democratize data access. 

```text
[User] --> (Natural Language Query) --> [LangChain Agent] 
                                              |
                                              v
[Streamlit UI] <--- (SQL Execution) <--- [DuckDB Engine]

🚀 Key Features & Innovations
Zero Hallucination Protocol: The LLM is strictly guarded. If the requested data does not exist within the Gold layer tables, the agent is programmed to refuse to answer rather than fabricate financial metrics.

Session-State Memory: The AI maintains conversational context, allowing users to ask follow-up questions naturally without losing previous data context.

Dynamic Data Bypassing: The UI features a Data Audit tab that reads directly from the data lake, preventing concurrency locking issues between the LLM database connection and the frontend visualization.

High-Performance Aggregation: Utilizing DuckDB's columnar engine ensures sub-second latency for analytical queries.

🛠️ Technology StackCategoryTechnology / FrameworkData OrchestrationApache Airflow, DockerData Processing & StorageDuckDB, Pandas, SQLArtificial IntelligenceLangChain, ChatGroq (Llama 3.3), Prompt EngineeringFrontend UIStreamlitEnvironment & ToolingPython 3.11, uv Package Manager, Git

⚙️ Local Setup & Execution
Prerequisites
Python 3.11+
uv package manager installed
Groq API Key

Installation

Clone the repository:
git clone [https://github.com/Tavarezzzz/boston-rides-ai-agent.git](https://github.com/Tavarezzzz/boston-rides-ai-agent.git)
cd boston-rides-ai-agent

Create the .env file and add your Groq API Key:
GROQ_API_KEY=your_api_key_here

Install dependencies using uv:
uv pip install -r requirements.txt

Launch the AI Web Interface:
uv run streamlit run app.py