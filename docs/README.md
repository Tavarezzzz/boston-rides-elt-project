Projeto ELT - Uber & Lyft Data Pipeline

Este projeto implementa um pipeline de Engenharia de Dados completo (ELT) utilizando a arquitetura Medalhão (Bronze, Silver, Gold).
Sobre o Projeto

O objetivo é analisar dados de corridas de aplicativos em Boston para responder perguntas de negócio como:
Qual serviço é mais barato por Km (Uber ou Lyft)?
Quais são as rotas mais caras?
Qual o impacto da tarifa dinâmica?
Tecnologias

Python: Linguagem principal.
DuckDB: Motor de processamento analítico (SQL).
Pandas: Leitura robusta de arquivos brutos.
Airflow: Orquestração das tarefas (código da DAG incluído).
Estrutura de Pastas

dags/: Contém a DAG do Airflow (elt.py).
src/: Scripts de transformação e extração.
data/: Armazenamento local dos dados (Data Lake).
Como Executar (Simulação Manual)

Instale as dependências:pip install -r requirements.txt


## 🏗 Arquitetura do Pipeline
O fluxo de dados segue o padrão **Medallion Architecture** (Bronze, Silver, Gold), garantindo governança e qualidade em cada etapa.

```mermaid
graph TD
    A[Fonte: CSV Kaggle] -->|Ingestão| B(Bronze: Raw Data)
    B -->|Limpeza com Pandas| C(Silver: Clean Data)
    C -->|Agregação com DuckDB| D(Gold: KPIs de Negócio)
