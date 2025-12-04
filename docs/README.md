# Projeto ELT - Uber & Lyft Data Pipeline

Este projeto implementa um pipeline de Engenharia de Dados completo (ELT) utilizando a arquitetura Medalhão (Bronze, Silver, Gold).

## Detalhes das Camadas:
- **Bronze** (Raw): Armazena o dado bruto (rideshare.csv) exatamente como veio da fonte.

- **Silver** (Clean): Script Python (transform_silver.py) utiliza Pandas para tratar inconsistências de encoding (UTF-16/UTF-8), remover nulos e tipar os dados.

- **Gold** (Analytics): Script Python (transform_gold.py) utiliza DuckDB para executar SQL analítico de alta performance, gerando os KPIs finais.

## Sobre o Projeto
O objetivo é analisar dados de corridas de aplicativos em Boston para responder perguntas de negócio como:
- Qual serviço é mais barato por Km (Uber ou Lyft)?
- Quais são as rotas mais caras?
- Qual o impacto da tarifa dinâmica?

## Tecnologias
- **Python**: Linguagem principal.
- **DuckDB**: Motor de processamento analítico (SQL).
- **Pandas**: Leitura robusta de arquivos brutos.
- **Airflow**: Orquestração das tarefas (código da DAG incluído).

## Estrutura de Pastas
- `dags/`: Contém a DAG do Airflow (`elt.py`).
- `src/`: Scripts de transformação e extração.
- `data/`: Armazenamento local dos dados (Data Lake).

## Como Executar (Simulação Manual)
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt

## 🏗 Arquitetura do Pipeline
O fluxo de dados segue o padrão **Medallion Architecture** (Bronze, Silver, Gold), garantindo governança e qualidade em cada etapa.

```mermaid
graph TD
    A[Fonte: CSV Kaggle] -->|Ingestão| B(Bronze: Raw Data)
    B -->|Limpeza com Pandas| C(Silver: Clean Data)
    C -->|Agregação com DuckDB| D(Gold: KPIs de Negócio)
