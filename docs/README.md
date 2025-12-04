# 🚖 Boston Rides ELT Pipeline (Uber vs Lyft)

> **Projeto Final de Engenharia de Dados**
> Pipeline ELT completo orquestrado via Airflow, aplicando a arquitetura Medalhão para análise de preços de mobilidade urbana.

---

## 📋 Sobre o Projeto
Este projeto implementa um pipeline de Engenharia de Dados completo (ELT) utilizando a arquitetura Medalhão (Bronze, Silver, Gold).

O objetivo é processar e analisar dados reais de corridas de **Uber** e **Lyft** em Boston (~700k registros) para responder perguntas de negócio como:
* Qual serviço é mais barato por Km (Uber ou Lyft)?
* Quais são as rotas mais caras?
* Qual o impacto da tarifa dinâmica no preço final?

---

## 🏗 Arquitetura e Camadas
O fluxo de dados segue o padrão **Medallion Architecture**, garantindo governança, rastreabilidade e qualidade em cada etapa física do Data Lake.

```mermaid
graph TD
    A[Fonte: CSV Kaggle] -->|Ingestão| B(Bronze: Raw Data)
    B -->|Limpeza com Pandas| C(Silver: Clean Data)
    C -->|Agregação com DuckDB| D(Gold: KPIs de Negócio)

Detalhe das Camadas:Camada Bronze (Raw):Armazena o dado bruto (rideshare_kaggle.csv) exatamente como veio da fonte.Função: Ingestão e preservação do histórico original.Camada Silver (Clean):Script: src/transform_silver.pyTecnologia: Python + Pandas.Tratamento: Foi identificado que o arquivo original possuía inconsistências de codificação (UTF-16 vs UTF-8). O script utiliza Pandas para corrigir o encoding, remover nulos e padronizar tipos.Camada Gold (Analytics):Script: src/transform_gold.pyTecnologia: Python + DuckDB.Lógica: Utiliza SQL analítico de alta performance para agregar os dados limpos e gerar os KPIs finais (Preço por Km, Rotas, Surge).🛠 Tecnologias UtilizadasPython 3.11: Linguagem principal de desenvolvimento.Apache Airflow: Orquestrador do pipeline (código da DAG incluso em dags/).DuckDB: Motor OLAP para processamento rápido de queries SQL na camada Gold.Pandas: Biblioteca utilizada na camada Silver para leitura robusta de arquivos.Git & GitHub: Versionamento e portfólio.📂 Estrutura de PastasO projeto está organizado da seguinte forma:Plaintext├── dags/
│   └── elt_pipeline.py    # Código da DAG do Airflow (Orquestração)
├── src/
│   ├── extract.py         # Script de validação de ingestão (Bronze)
│   ├── transform_silver.py# Script de limpeza e tratamento (Silver)
│   ├── transform_gold.py  # Script de geração de KPIs (Gold)
│   └── analise_final.py   # Script auxiliar para visualizar resultados
├── data/
│   ├── bronze/            # Armazenamento do CSV bruto
│   ├── silver/            # Armazenamento dos dados tratados
│   └── gold/              # Armazenamento das tabelas finais (KPIs)
└── requirements.txt       # Lista de dependências do projeto
📊 Resultados AlcançadosApós a execução do pipeline, a camada Gold entregou os seguintes insights de negócio:KPIDescriçãoPreço por KmComparativo direto de eficiência de custo entre Uber e Lyft.Tarifa DinâmicaAnálise de quanto o preço sobe conforme o multiplicador de demanda (Surge).Top RotasIdentificação das origens e destinos com maior ticket médio em Boston.🚀 Como Executar (Simulação Manual)Devido a restrições de ambiente (Windows sem Docker nativo), o pipeline foi validado executando os scripts das tarefas sequencialmente:Instale as dependências:Bashpip install -r requirements.txt
Execute a Limpeza (Bronze -> Silver):Bashpython src/transform_silver.py
Execute as Agregações (Silver -> Gold):Bashpython src/transform_gold.py
Visualize o Relatório Final:Bashpython src/analise_final.py
