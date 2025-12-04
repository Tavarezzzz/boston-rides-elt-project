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
