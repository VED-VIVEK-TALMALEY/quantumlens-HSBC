<!-- -------------------------------------------------------------------
Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
This project and its source code are strictly proprietary.
Unauthorized copying, distribution, or use is strictly prohibited.
------------------------------------------------------------------- -->

# QuantumLens

### *AI-Powered Global Banking Intelligence & Risk Observatory*

[![Python Version](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.138.1-teal?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Supabase](https://img.shields.io/badge/Supabase-2.31.0-emerald?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Oracle DB](https://img.shields.io/badge/Oracle_DB-19c%2B-red?style=for-the-badge&logo=oracle&logoColor=white)](https://www.oracle.com)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](https://opensource.org/licenses/MIT)

**HSBC QuantumLens** is an institutional-grade financial data platform that resembles an internal strategic war room used by COO, CRO, or treasury teams. By analyzing Q1 results (including Net Interest Income volatility, Expected Credit Losses provisioning, capital CET1 compression, and HNWI wealth inflows into Asia), QuantumLens shifts traditional financial reporting from static data visualizers into an **AI-native banking intelligence operating system**.

The platform is designed like a **Bloomberg Terminal × Palantir × McKinsey War Room**, integrating data ingestion pipelines, financial knowledge graphs, RAG call intelligence, scenario forecasters, executive war-room dashboards, and multi-agent AI copilots.

---

## 6-Layer Architecture Overview

```mermaid
graph TD
    %% Define Nodes
    subgraph ClientLayer ["Layer 5: Apache Superset War Rooms (frontend/)"]
        UI["Next.js Dashboards UI<br>(Pulse, Wealth, Stress, Contagion)"]
    end

    subgraph APILayer ["Layer 6: AI Copilot Router (backend/src/api/)"]
        FastAPI["FastAPI Web Router"]
    end

    subgraph ForecastingLayer ["Layer 4: Advanced Forecasting Engine (ml_models/)"]
        Forecast["Forecaster<br>(Prophet / XGBoost / LSTMs)"]
    end

    subgraph AILayer ["Layer 3: AI Call Intelligence (backend/src/rag/)"]
        Chroma[("ChromaDB Vector Store")]
        FinBERT["FinBERT NLP Pipeline<br>(Anxiety / Sentiment index)"]
        Groq["Groq Cloud API<br>(llama-3.3-70b-versatile)"]
    end

    subgraph KnowledgeGraph ["Layer 2: Financial Knowledge Graph (neo4j/)"]
        Neo4j[("Neo4j Graph Database<br>(Risk Contagion Nodes)")]
    end

    subgraph DataEngineering ["Layer 1: Data Engineering Pipeline (backend/src/ingestion/)"]
        Reader["Workbook Reader"]
        Scanner["Sheet Scanner"]
        Extractor["Metric Extractor"]
        Mapper["Period Mapper"]
        Builder["KPI Builder"]
    end

    subgraph StorageLayer ["Database Warehouse Layer (backend/warehouse/)"]
        Supabase[("Supabase (PostgreSQL 15)<br>[JSONB arrays]")]
        Oracle[("Oracle Database 19c<br>[Period observations]")]
    end

    %% Define Connections
    UI <-->|HTTP REST JSON| FastAPI
    FastAPI <-->|SQL Queries| Supabase
    FastAPI <-->|Retrieve Context| Chroma
    
    %% Ingestion Flow
    xlsx["Raw Excel Files (.xlsx)"] --> Reader
    Reader --> Scanner
    Scanner --> Extractor
    Extractor --> Mapper
    Mapper --> Builder
    Builder -->|Batch Upserts| Supabase
    Builder -->|Insert Rows| Oracle
    Builder -->|Stress nodes| Neo4j
    
    %% Vector Ingestion Flow
    Supabase -->|SQL Extract| FinBERT
    FinBERT -->|Dense Embeddings| Chroma
    
    %% RAG Pipeline Flow
    FastAPI -->|Question Query| Chroma
    Chroma -->|Relevant Context Docs| FastAPI
    FastAPI -->|Context + Prompt| Groq
    Groq -->|Context-Grounded Answer| FastAPI
    
    %% Forecasting Connection
    Oracle --> Forecast
    Forecast --> UI
    
    %% Styles
    classDef client fill:#1f77b4,stroke:#333,stroke-width:2px,color:#fff;
    classDef api fill:#2ca02c,stroke:#333,stroke-width:2px,color:#fff;
    classDef storage fill:#9467bd,stroke:#333,stroke-width:2px,color:#fff;
    classDef etl fill:#ff7f0e,stroke:#333,stroke-width:2px,color:#fff;
    classDef ai fill:#d62728,stroke:#333,stroke-width:2px,color:#fff;
    classDef forecast fill:#e377c2,stroke:#333,stroke-width:2px,color:#fff;
    classDef kg fill:#bcbd22,stroke:#333,stroke-width:2px,color:#fff;
    
    class UI client;
    class FastAPI api;
    class Reader,Scanner,Extractor,Mapper,Builder etl;
    class Supabase,Oracle storage;
    class Chroma,FinBERT,Groq ai;
    class Forecast forecast;
    class Neo4j kg;
```

### Layer Matrix

| Layer | Responsibility | Primary Technologies | File Locations |
| :--- | :--- | :--- | :--- |
| **Layer 1: Pipeline** | Ingestion of raw reports, grid scanning, name normalization, and data cleaning. | Python, Pandas, Openpyxl | `backend/src/ingestion/` |
| **Layer 2: Graph** | Modeling counterparty links, exposures, and systemic contagion paths. | Neo4j, Cypher Queries | `neo4j/` |
| **Layer 3: NLP** | Sentiment analysis, semantic drift mapping, and executive anxiety indexing. | FinBERT, spaCy, ChromaDB | `backend/src/rag/` |
| **Layer 4: Forecasting**| Generating predictions for NII, CET1, and deposits under macro rate scenario stress tests. | Prophet, XGBoost, LSTMs | `ml_models/` |
| **Layer 5: BI Portal** | Executive war-room dashboards (Pulse, Wealth, Stress, Strategy, Contagion). | Next.js, React, Tailwind, Recharts | `frontend/` |
| **Layer 6: AI Copilot**| Multi-Agent orchestration matching SQL database metrics with transcript contexts. | FastAPI, LangChain, Groq API | `backend/src/api/` |

---

## Technical Stack Summary

| Component | Selected Technologies | Description / Role |
| :--- | :--- | :--- |
| **Data Ingestion** | Kafka, Airflow, dbt, Pandas | Event streaming, workflow coordination, and transformation. |
| **Storage Layer** | PostgreSQL (Supabase) & Oracle DB | PostgreSQL stores time-series JSONB arrays; Oracle flattens observations. |
| **AI & Retrieval** | SentenceTransformers, ChromaDB, Groq Cloud | Local BAAI embeddings, local persistent vector collections, Llama-3.3. |
| **Frontend UI** | Next.js 15, Recharts, TailwindCSS | App router portal, interactive visualizations, styling framework. |
| **Infrastructure** | Docker, Kubernetes | Containerized microservices layouts and scaling. |

---

## Live Deployments

| Component | Target URL | Platform Host | Status |
| :--- | :--- | :--- | :--- |
| **Analytics Portal** | [https://quantumlens-hsbc.vercel.app](https://quantumlens-hsbc.vercel.app) | Vercel | Under Integration |
| **REST API Server** | [https://quantumlens-api.render.com](https://quantumlens-api.render.com) | Render | Operational |
| **API Swagger Specs**| [https://quantumlens-api.render.com/docs](https://quantumlens-api.render.com/docs) | Render | Operational |

---

## Local Ingestion and API Setup

### Setup Steps Tabular Guide

| Step | Action | Powershell / Terminal Command | Notes |
| :--- | :--- | :--- | :--- |
| **1** | Clone Project | `git clone https://github.com/VED-VIVEK-TALMALEY/quantumlens-HSBC.git` | Downloads repository. |
| **2** | Sandbox Env | `python -m venv .venv` | Creates virtual env. |
| **3** | Activate Env | `source .venv/bin/activate` or `.venv\Scripts\Activate.ps1` | Activates virtual env. |
| **4** | Install Modules | `pip install -r backend/requirements.txt` | Restores ETL, FastAPI, and AI dependencies. |
| **5** | Local Configs | `copy backend/.env.example backend/.env` | Inject Supabase and Groq keys. |
| **6** | Ingest Excel | `python backend/src/ingestion/sheet_scanner.py` | Extracts cell coordinates to JSON files. |
| **7** | Load Database | `python backend/warehouse/data_loader.py` | Batches metrics payload to Supabase metrics table. |
| **8** | Load Oracle | `python backend/warehouse/load_to_oracle.py` | Transforms and inserts observations to Oracle. |
| **9** | Launch REST API| `uvicorn backend.src.api.main:app --reload --port 8000` | Boots FastAPI reloading server on port 8000. |

---

## Environment Variables Configuration

> [!WARNING]
> Ensure all API keys are kept secure and never committed to public repositories.

| Variable Name | Required | Description | Default Local |
| :--- | :--- | :--- | :--- |
| `SUPABASE_URL` | YES | Endpoint for Supabase Database REST interface. | `https://<YOUR_PROJECT_ID>.supabase.co` |
| `SUPABASE_KEY` | YES | Service Role administrative key to bypass RLS policies. | `<YOUR_SUPABASE_SERVICE_ROLE_KEY>` |
| `GROQ_API_KEY` | YES | API token for Groq Cloud LLM completions. | `<YOUR_GROQ_API_KEY>` |
| `VECTOR_DB_PATH` | NO | Local directory to persist ChromaDB index assets. | `backend/src/rag/vector_db` |
| `EMBEDDINGS_PATH`| NO | Local file path caching pre-computed embeddings. | `backend/data/generated/embeddings.json` |
| `EMBEDDING_MODEL`| NO | HuggingFace embedding model ID. | `sentence-transformers/all-MiniLM-L6-v2` |
| `TOP_K` | NO | Top document count returned during semantic search retrieval. | `5` |

---

## Executive War Rooms (Next.js Portal)

The dashboard frontend ([frontend/](frontend/)) structures metrics into five interactive screens:

| Dashboard View | Primary Metrics Tracked | Interactivity Features |
| :--- | :--- | :--- |
| **Global Banking Pulse** | NII, CET1 capital ratio, RoTE, loan growth rates. | Cross-filtering, regional heatmaps, animated charts. |
| **Wealth Migration** | Asia wealth inflows ($34B), net new money ($39B), wealth fees growth (+15%). | Capital concentration, HNWI wealth migration maps. |
| **Credit Stress Radar** | ECL guidance (~45bps), sector impairments, fraud exposures. | Macro shock stress test simulators (FX, oil spikes, rate cuts). |
| **Strategic Transformation**| Disposals, simplification savings ($1.5B), synergy metrics ($0.5B). | Dynamic KPI metric cards, progress metrics charts. |
| **Contagion Network** | Exposures, liquidity links, counterparty relations. | Interactive Neo4j node graph layouts representing stress flows. |

---

## Multi-Agent AI Financial Copilot

Queries targeting the backend REST API `/ask` route are processed by a custom Multi-Agent Orchestrator:

```mermaid
graph TD
    User([User Request]) --> Planner{Planner Agent}
    Planner -->|Intent: SQL| SQLAgent[SQL Agent]
    Planner -->|Intent: RAG| RAGAgent[RAG Agent]
    SQLAgent --> Oracle[(Oracle Database)]
    RAGAgent --> Chroma[(ChromaDB Vector Store)]
    Oracle --> Synthesizer[Response Synthesizer]
    Chroma --> Synthesizer
    Synthesizer --> Groq[Groq Llama-3.3]
    Groq --> FinalResponse([Context-Grounded Board Report])
```

| Agent | Module Path | Purpose |
| :--- | :--- | :--- |
| **Planner** | [planner.py](backend/src/agents/planner.py) | Deconstructs query intent (`SQL` vs `RAG` vs `Chart`). |
| **SQL Agent** | [sql_agent.py](backend/src/agents/sql_agent.py) | Executes query parameters against Oracle/Supabase schemas. |
| **RAG Agent** | [rag_agent.py](backend/src/agents/rag_agent.py) | Queries ChromaDB vectors to find semantic transcript matches. |
| **Chart Agent**| [chart_agent.py](backend/src/agents/chart_agent.py) | Formats query metric lists into structured Recharts coordinates. |
| **Orchestrator**| [orchestrator.py](backend/src/agents/orchestrator.py) | Integrates agent states and prompts Groq LLM for final delivery. |

---

## Contributing

We welcome contributions to improve HSBC QuantumLens. Open a pull request or file issues under the repository tracker.

---

## License

This project is open-source software licensed under the MIT License.

---

## Complete Documentation Reference

Expand the sections below to view the full contents of all other documentation files in this repository.

<details>
<summary><b>System Architecture Specification (docs/architecture/architecture.md)</b></summary>

# System Architecture Specification

This document details the architectural layout, system layers, and component interactions of **QuantumLens** (also known as *HSBC Atlas* or *Project Basilisk*), an institutional-grade banking intelligence platform.

For a high-level overview, deployment metrics, or setup instructions, see the primary [README.md](README.md).

---

## 6-Layer Architecture Overview

QuantumLens is built on six decoupled engineering layers. This decoupling ensures that vector-indexed LLM reasoning and graph contagion modeling run independently of core transactional databases and ETL workflows.

```mermaid
graph TD
    %% Define Nodes
    subgraph ClientLayer ["Layer 5: Apache Superset War Rooms (frontend/)"]
        UI["Next.js Dashboards UI<br>(Pulse, Wealth, Stress, Contagion)"]
    end

    subgraph APILayer ["Layer 6: AI Copilot Router (backend/src/api/)"]
        FastAPI["FastAPI Web Router"]
    end

    subgraph ForecastingLayer ["Layer 4: Advanced Forecasting Engine (ml_models/)"]
        Forecast["Forecaster<br>(Prophet / XGBoost / LSTMs)"]
    end

    subgraph AILayer ["Layer 3: AI Call Intelligence (backend/src/rag/)"]
        Chroma[("ChromaDB Vector Store")]
        FinBERT["FinBERT NLP Pipeline<br>(Anxiety / Sentiment index)"]
        Groq["Groq Cloud API<br>(llama-3.3-70b-versatile)"]
    end

    subgraph KnowledgeGraph ["Layer 2: Financial Knowledge Graph (neo4j/)"]
        Neo4j[("Neo4j Graph Database<br>(Risk Contagion Nodes)")]
    end

    subgraph DataEngineering ["Layer 1: Data Engineering Pipeline (backend/src/ingestion/)"]
        Reader["Workbook Reader"]
        Scanner["Sheet Scanner"]
        Extractor["Metric Extractor"]
        Mapper["Period Mapper"]
        Builder["KPI Builder"]
    end

    subgraph StorageLayer ["Database Warehouse Layer (backend/warehouse/)"]
        Supabase[("Supabase (PostgreSQL 15)<br>[JSONB arrays]")]
        Oracle[("Oracle Database 19c<br>[Period observations]")]
    end

    %% Define Connections
    UI <-->|HTTP REST JSON| FastAPI
    FastAPI <-->|SQL Queries| Supabase
    FastAPI <-->|Retrieve Context| Chroma
    
    %% Ingestion Flow
    xlsx["Raw Excel Files (.xlsx)"] --> Reader
    Reader --> Scanner
    Scanner --> Extractor
    Extractor --> Mapper
    Mapper --> Builder
    Builder -->|Batch Upserts| Supabase
    Builder -->|Insert Rows| Oracle
    Builder -->|Stress nodes| Neo4j
    
    %% Vector Ingestion Flow
    Supabase -->|SQL Extract| FinBERT
    FinBERT -->|Dense Embeddings| Chroma
    
    %% RAG Pipeline Flow
    FastAPI -->|Question Query| Chroma
    Chroma -->|Relevant Context Docs| FastAPI
    FastAPI -->|Context + Prompt| Groq
    Groq -->|Context-Grounded Answer| FastAPI
    
    %% Forecasting Connection
    Oracle --> Forecast
    Forecast --> UI
    
    %% Styles
    classDef client fill:#1f77b4,stroke:#333,stroke-width:2px,color:#fff;
    classDef api fill:#2ca02c,stroke:#333,stroke-width:2px,color:#fff;
    classDef storage fill:#9467bd,stroke:#333,stroke-width:2px,color:#fff;
    classDef etl fill:#ff7f0e,stroke:#333,stroke-width:2px,color:#fff;
    classDef ai fill:#d62728,stroke:#333,stroke-width:2px,color:#fff;
    classDef forecast fill:#e377c2,stroke:#333,stroke-width:2px,color:#fff;
    classDef kg fill:#bcbd22,stroke:#333,stroke-width:2px,color:#fff;
    
    class UI client;
    class FastAPI api;
    class Reader,Scanner,Extractor,Mapper,Builder etl;
    class Supabase,Oracle storage;
    class Chroma,FinBERT,Groq ai;
    class Forecast forecast;
    class Neo4j kg;
```

---

## Technical Layers Matrix

| Layer | Responsibility | Input Shape | Output Shape | Data Store Target |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1: Pipeline** | Parsing Excel cells, stripping merged headers, and outputting JSON coordinates. | Raw Excel files (`.xlsx`) | Cleaned JSON coordinate maps | File cache / local disks |
| **Layer 2: Graph** | Modeling counterparty risk, wealth flows, and geopolitical contagion propagation paths. | Structured KPI metrics | Entity node networks and exposures | Neo4j Graph DB |
| **Layer 3: NLP** | Executing FinBERT sentiment classification and measuring management anxiety indices. | Earnings transcripts, executive remarks | Confidence and risk indexes | ChromaDB Vector Store |
| **Layer 4: Forecast** | Generating NII, RoTE, and credit provision forecasts under macroeconomic scenario stress tests. | Relational metrics history | Predictive timeline indicators | Warehouse databases |
| **Layer 5: UI Portal** | Hosting executive dashboards and rendering Recharts visualizations. | User selections, REST query parameters | Interactive dashboards views | Browser local state / caches |
| **Layer 6: AI Copilot**| Planning query intent and combining SQL metrics with semantic search documents. | Natural language questions | Factual, source-attributed text replies | Local host runtime |

---

## Modular System Breakdown

The system modules are partitioned as follows:

| Script / Module | Architecture Layer | Core Function | Primary Python Packages | File Path |
| :--- | :--- | :--- | :--- | :--- |
| **workbook_reader.py** | Layer 1: Data Pipeline | Reads binary workbooks in read-only mode to prevent memory leak issues. | `pandas`, `openpyxl` | [workbook_reader.py](backend/src/ingestion/workbook_reader.py) |
| **sheet_scanner.py** | Layer 1: Data Pipeline | Parses worksheets cell-by-cell and fills merged header regions programmatically. | `pandas`, `numpy` | [sheet_scanner.py](backend/src/ingestion/sheet_scanner.py) |
| **metric_extractor.py**| Layer 1: Data Pipeline | Normalizes names to a centralized config map in constant O(1) time. | `re`, `json` | [metric_extractor.py](backend/src/ingestion/metric_extractor.py) |
| **value_extractor.py** | Layer 1: Data Pipeline | Isolates floats, filtering out string footnotes or empty indicators. | `pandas`, `numpy` | [value_extractor.py](backend/src/ingestion/value_extractor.py) |
| **period_mapper.py** | Layer 1: Data Pipeline | Maps spreadsheet columns to sequential chronological period indexes. | `json` | [period_mapper.py](backend/src/transformation/period_mapper.py) |
| **kpi_builder.py** | Layer 1: Data Pipeline | Compiles metrics trend flags (`up`, `down`, `flat`) and timestamps records. | `datetime` | [kpi_builder.py](backend/src/transformation/kpi_builder.py) |
| **data_loader.py** | Layer 1: Data Pipeline | Batches records to Supabase tables using natural key upsert operations. | `supabase` | [data_loader.py](backend/warehouse/data_loader.py) |
| **load_to_oracle.py** | Layer 1: Data Pipeline | Flattens observations and uploads data rows to Oracle Database. | `oracledb` | [load_to_oracle.py](backend/warehouse/load_to_oracle.py) |
| **query_service.py** | Layer 6: AI Copilot | Wraps database queries, providing metrics arrays to FastAPI routers. | `oracledb` | [query_service.py](backend/warehouse/query_service.py) |
| **embedding_generator.py**| Layer 3: AI Intelligence | Creates vector embeddings from metrics metadata using local BAAI models. | `sentence-transformers` | [embedding_generator.py](backend/src/rag/embedding_generator.py) |
| **vector_loader.py** | Layer 3: AI Intelligence | Registers vector collections in ChromaDB and handles index persistence. | `chromadb` | [vector_loader.py](backend/src/rag/vector_loader.py) |
| **retrieval_engine.py**| Layer 3: AI Intelligence | Performs cosine searches on vectorized metrics with distance filters. | `chromadb` | [retrieval_engine.py](backend/src/rag/retrieval_engine.py) |
| **rag_pipeline.py** | Layer 6: AI Copilot | Orchestrates system prompts, injecting contexts for LLM execution. | `groq` | [rag_pipeline.py](backend/src/rag/rag_pipeline.py) |

---

## Detailed Data Flows & Sequence Diagrams

### 1. Ingestion and ETL Pipeline Data Flow

The following sequence illustrates the stages of processing raw spreadsheets into database tables:

```mermaid
sequenceDiagram
    autonumber
    participant Excel as Raw Spreadsheet (.xlsx)
    participant Reader as Ingestion Layer (workbook_reader.py)
    participant Scanner as Ingestion Layer (sheet_scanner.py)
    participant Extractor as Transformation (metric_extractor.py)
    participant Builder as Transformation (kpi_builder.py)
    participant DB as Warehouse (Supabase/Postgres)
    participant Oracle as Warehouse (Oracle DB)
    participant Neo4j as Graph Database (Neo4j)

    Excel->>Reader: File Path of workbook
    activate Reader
    Reader->>Scanner: Pandas ExcelFile representation
    deactivate Reader
    activate Scanner
    Scanner->>Extractor: JSON Row Coordinates with raw strings
    deactivate Scanner
    activate Extractor
    Extractor->>Builder: Matched Raw Metrics with config mappings
    deactivate Extractor
    activate Builder
    Builder->>DB: Upsert Ingested KPI Payload (JSONB array structure)
    Builder->>Oracle: Insert sequential rows (single period observations)
    Builder->>Neo4j: Create exposure nodes and dependencies
    deactivate Builder
```

---

### 2. Multi-Agent RAG Query Sequence

This sequence diagram illustrates the steps when a user queries the API for financial analytics:

```mermaid
sequenceDiagram
    autonumber
    actor User as Client App (API/Web)
    participant API as FastAPI REST Router (main.py)
    participant Planner as Planner Agent (planner.py)
    participant SQLAgent as SQL Agent (sql_agent.py)
    participant RAGAgent as RAG Agent (rag_agent.py)
    participant Oracle as Oracle Database
    participant VectorDB as Vector Store (ChromaDB Local)
    participant LLM as Inference Engine (Groq Cloud)

    User->>API: POST /ask { "question": "..." }
    activate API
    API->>Planner: parse_query(question)
    activate Planner
    Planner-->>API: Intent Matrix: {use_sql: true, use_rag: true}
    deactivate Planner
    
    API->>SQLAgent: get_metrics_sql(question)
    activate SQLAgent
    SQLAgent->>Oracle: Query historical values
    Oracle-->>SQLAgent: SQL data rows
    SQLAgent-->>API: Structured metrics values
    deactivate SQLAgent

    API->>RAGAgent: search_context(question)
    activate RAGAgent
    RAGAgent->>VectorDB: search_embeddings(question)
    VectorDB-->>RAGAgent: Retrived text documents
    RAGAgent-->>API: Context documents strings
    deactivate RAGAgent

    API->>LLM: Complete Response (System Prompt + SQL Data + Context Docs + Question)
    activate LLM
    LLM-->>API: Grounded financial response text
    deactivate LLM

    API-->>User: HTTP 200 OK Response (answer, sources)
    deactivate API
```

---

## Related Documentation
* [Primary Readme](README.md): Project overview, installation scripts, API reference.
* [Database Schema (Data Dictionary)](docs/features/ingestion/data_dictionary.md): Detailed columns description, indices, and constraints.
* [KPI Catalog Mapping](docs/features/rag/kpi_catalog.md): Synonym dictionaries and lookup rules.


</details>

<details>
<summary><b>Database Design & Data Dictionary (docs/features/ingestion/data_dictionary.md)</b></summary>

# Database Design & Data Dictionary

This document details the relational data warehouse design, table schemas, indices, and database constraints of **QuantumLens**.

For deployment steps or API integration hooks, see the primary [README.md](README.md). For system architecture diagrams, see [architecture.md](docs/architecture/architecture.md).

---

## Database Design Rationale

QuantumLens supports two target database engines to cater to both cloud-native applications and corporate environments:

| Database Engine | Storage Model | Core Advantage | Primary Target |
| :--- | :--- | :--- | :--- |
| **Supabase (PostgreSQL 15)** | **Hybrid JSONB / Row** | Stores variable-length time-series data inside a single record as a JSONB array, preventing schema modification and table fragmentation during quarter expansions. | FastAPI API Client / RAG Search |
| **Oracle Database** | **Fully Normalized Relational** | Flattens time-series observations into individual rows (one row per period) to allow traditional OLAP analysis and BI report generations. | Enterprise Systems / OLAP Analytics |

---

## Side-by-Side Schema Comparison

The following table contrasts the two storage layouts for the same metric:

| Attribute | Supabase (PostgreSQL 15) | Oracle Database |
| :--- | :--- | :--- |
| **Table Name** | `metrics` | `metrics` |
| **Primary Key** | `id` (Auto-increment `SERIAL`) | `id` (Auto-increment `NUMBER`) |
| **Unique Constraint** | `metric_id` (enforces one record per KPI) | None (allows multiple period rows per KPI) |
| **Time-Series Column** | `period_values` (storing JSONB array of objects) | `period` (VARCHAR2) & `value` (NUMBER) |
| **Metadata Columns** | `source_workbook`, `sheet_name`, `row_number` | `source_workbook`, `sheet_name`, `row_number` |
| **Audit Column** | `created_at` (TIMESTAMP WITH TIME ZONE) | `category` (VARCHAR2), `unit` (VARCHAR2) |

---

## Detailed Data Dictionaries

### 1. Supabase (PostgreSQL 15) Schema Details

The `metrics` table stores normalized KPI records parsed by the ETL loader.

#### Columns Dictionary

| Column Name | SQL Type | Nullable | Default | Description & Constraint |
| :--- | :--- | :--- | :--- | :--- |
| **id** | `SERIAL` | NO | `nextval()` | Auto-incrementing relational key. |
| **metric_id** | `INTEGER` | NO | None | Unique business metric identifier mapping (Unique Constraint). |
| **metric_name** | `TEXT` | NO | None | Normalized canonical name mapped from config dictionary. |
| **abbreviation**| `TEXT` | YES | `NULL` | Shortened acronym name (e.g. `nii` for net interest income). |
| **period_values**| `JSONB` | NO | None | Time-series values array of objects: `[{"period_index": 1, "value": 8945}]`. |
| **source_workbook**| `TEXT` | NO | None | Source Excel file name. |
| **sheet_name** | `TEXT` | NO | None | Tab sheet name where record was found. |
| **row_number** | `INTEGER` | NO | None | Spreadsheet row index (1-indexed). |
| **created_at** | `TIMESTAMP` | NO | `now()` | Date and timestamp of record insertion (Timezone aware). |

#### SQL Schema Definition
```sql
CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    metric_id INTEGER UNIQUE NOT NULL,
    metric_name TEXT NOT NULL,
    abbreviation TEXT,
    period_values JSONB NOT NULL,
    source_workbook TEXT NOT NULL,
    sheet_name TEXT NOT NULL,
    row_number INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

#### Query Optimizations (PostgreSQL Indices)
| Index Name | Column Indexed | Type | Core Benefit |
| :--- | :--- | :--- | :--- |
| `metrics_pkey` | `id` | B-Tree | Speeds up direct row access by primary key. |
| `idx_metric_id` | `metric_id` | B-Tree | Optimizes exact matching lookups (e.g., `/metric/{metric_id}`). |
| `idx_metric_name`| `metric_name` | B-Tree | Speeds up exact and sorting lookups on canonical names. |

---

### 2. Oracle Database Schema Details

The `metrics` table stores normalized observations flattened by chronological period.

#### Columns Dictionary

| Column Name | SQL Type | Nullable | Primary Key | Description & Defaults |
| :--- | :--- | :--- | :--- | :--- |
| **id** | `NUMBER` | NO | YES | Generated Always as Identity database key. |
| **metric_id** | `NUMBER` | YES | NO | Associated business metric identifier. |
| **metric_name** | `VARCHAR2(200)` | YES | NO | Normalized canonical name of the metric. |
| **abbreviation**| `VARCHAR2(50)` | YES | NO | Associated short name code. |
| **sheet_name** | `VARCHAR2(200)` | YES | NO | Tab worksheet name where record was located. |
| **source_workbook**| `VARCHAR2(200)` | YES | NO | Source workbook filename. |
| **row_number** | `NUMBER` | YES | NO | Source sheet row coordinate. |
| **period** | `VARCHAR2(20)` | YES | NO | Chronological reporting index string (e.g., "1", "2"). |
| **value** | `NUMBER` | YES | NO | Numerical observation value for this period. |
| **unit** | `VARCHAR2(20)` | YES | NO | Optional unit annotation. |
| **category** | `VARCHAR2(100)` | YES | NO | Category classifier, defaults to `'Financial KPI'`. |

#### SQL Schema Definition
```sql
CREATE TABLE metrics (
    id NUMBER GENERATED ALWAYS AS IDENTITY,
    metric_id NUMBER,
    metric_name VARCHAR2(200),
    abbreviation VARCHAR2(50),
    sheet_name VARCHAR2(200),
    source_workbook VARCHAR2(200),
    row_number NUMBER,
    period VARCHAR2(20),
    value NUMBER,
    unit VARCHAR2(20),
    category VARCHAR2(100),
    CONSTRAINT metrics_pk PRIMARY KEY(id)
);
```

---

## Future Schema Extensions

To transition QuantumLens into a multi-tenant enterprise portal, the database will be extended with the following schemas (tabulated):

| Table Name | Target Engine | Purpose | Relationship | Key Fields |
| :--- | :--- | :--- | :--- | :--- |
| **users** | PostgreSQL | Manages client login accounts and dashboard access roles. | None | `id` (UUID Primary Key), `email` (Unique) |
| **dashboards** | PostgreSQL | Stores user-configured dashboard arrangements and layouts. | M:1 with `users` | `id` (Primary Key), `user_id` (Foreign Key) |
| **reports** | PostgreSQL | Caches statically compiled financial summaries and snaps. | M:1 with `dashboards`| `id` (Primary Key), `dashboard_id` (Foreign Key) |
| **chat_history** | PostgreSQL | Stores natural language question and answers for session checks. | M:1 with `users` | `id` (Primary Key), `session_id` (Indexed) |

---

## Related Documentation
* [Primary Readme](README.md): Project overview, installation scripts, API reference.
* [System Architecture Spec](docs/architecture/architecture.md): System layers overview and Mermaid diagrams.
* [KPI Catalog & Normalization Rules](docs/features/rag/kpi_catalog.md): Dictionary lookup configurations.


</details>

<details>
<summary><b>KPI Catalog & Normalization Logic (docs/features/rag/kpi_catalog.md)</b></summary>

# KPI Catalog & Normalization Logic

This document details the metric normalization engine, lookup dictionary catalog entries, and target mapping strategies utilized by **QuantumLens**.

For system architecture layouts, see [architecture.md](docs/architecture/architecture.md). For table details, see [data_dictionary.md](docs/features/ingestion/data_dictionary.md).

---

## The Normalization Engine

In financial analytics, different business sheets and reporting periods frequently reference the same underlying metric using distinct labels. For example, "Net Interest Income", "Net Interest", and "NII" refer to the same metric.

To handle this variation, the pipeline runs a string-standardization flow:

```text
  Raw Input Text               Clean & Normalize              Dictionary Hash Map             Normalized Output
" Net Interest Income " ──► "net interest income" ──► {"net interest income": ID: 1} ──► ID: 1, net_interest_income
```

### Ingestion Matching Workflow Table
| Step | Phase | Action | System Method | Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Cell Extraction | Read row list values from raw pandas structures. | `pandas.read_excel()` | `O(1)` |
| **2** | Normalization | Strip margins, cast strings to lowercase, trim spaces, and replace punctuation. | String cleanup regex | `O(M)` (M is string length) |
| **3** | Dictionary Matching| Probe the dictionary cache hash-map using the clean token. | Hash map check against JSON keys | `O(1)` |
| **4** | Record Hydration | If matched, extract values, map period indexes, and build target KPI record. | JSON serialization & timestamping | `O(P)` (P is period count) |

---

## Complete Catalog Lookup Dictionary

The system loads mapping configurations from [metric_dictionary.json](backend/src/ingestion/metric_dictionary.json). Below is the complete catalog:

| Metric ID | Normalized Canonical Name | Abbreviation Code | Target Worksheet Context / Description |
| :--- | :--- | :--- | :--- |
| **1** | `net_interest_income` | `nii` | Banking net yield / Group Income Statement |
| **2** | `net_fee_income` | `nfi` | Non-interest fees / Group Income Statement |
| **3** | `other_operating_income` | `ooi` | Miscellaneous operating streams |
| **4** | `net_operating_income` | `noi` | Total net revenue after ECL |
| **5** | `expected_credit_losses` | `ecl` | Credit risk impairments and charges |
| **6** | `total_operating_expenses` | `toe` | Overhead, administrative, and system costs |
| **7** | `profit_before_tax` | `pbt` | Core operating profit pre-taxation |
| **8** | `profit_after_tax` | `pat` | Net income after tax deductions |
| **9** | `profit_attributable_to_ordinary_shareholders` | `paos` | Net income available for ordinary equity |
| **10** | `return_on_average_equity` | `roae` | Profitability indicator relative to average equity |
| **11** | `return_on_average_tangible_equity` | `rote` | Profitability indicator relative to tangible equity |
| **12** | `earnings_per_share` | `eps` | Basic earnings allocated per ordinary share |
| **13** | `dividends_per_share` | `dps` | Declared dividends distributed per share |
| **14** | `total_assets` | `ta` | Aggregate banking books assets / Balance Sheet |
| **15** | `total_liabilities` | `tl` | Aggregate outstanding liabilities / Balance Sheet |
| **16** | `total_shareholders_equity` | `tse` | Net asset value of the banking group |
| **17** | `loans_and_advances_to_customers_net` | `lacn` | Net customer credit books / Balance Sheet |
| **18** | `customer_accounts` | `ca` | Total customer deposits / Balance Sheet |
| **19** | `risk_weighted_assets` | `rwa` | Assets weighted by risk multipliers / Basel capital |
| **20** | `common_equity_tier_1_capital` | `cet1` | High-quality regulatory capital capital base |
| **21** | `common_equity_tier_1_ratio` | `cet1r` | CET1 capital divided by total RWA |
| **22** | `tier_1_ratio` | `t1r` | Tier 1 capital divided by total RWA |
| **23** | `total_capital_ratio` | `tcr` | Total capital divided by total RWA |
| **24** | `leverage_ratio` | `lr` | Tier 1 capital divided by total leverage exposure |
| **25** | `net_interest_margin` | `nim` | Net interest income relative to earning assets |
| **26** | `tangible_net_asset_value` | `tnav` | Total equity excluding intangible assets |
| **27** | `net_asset_value_per_share` | `navps` | Net tangible assets allocated per share |
| **28** | `banking_net_interest_income` | `bnii` | Segmented commercial banking net interest yield |
| **29** | `wholesale_transaction_banking_revenue` | `wtbr` | Corporate banking transaction fees revenue |
| **30** | `wealth_revenue` | `wr` | Asset management and private banking revenues |
| **31** | `revenue` | `rev` | Top-line sales and revenues |
| **32** | `deposits` | `dep` | Customer deposits aggregate |
| **33** | `wealth_net_new_money` | `wnnm` | Assets under management net inflow indicators |
| **34** | `cost_efficiency_ratio` | `cer` | Operating expenses divided by operating income |
| **35** | `operating_expenses` | `opex` | General operating costs |
| **36** | `credit_loss_ratio` | `clr` | Expected credit losses relative to gross loans |

---

## Normalization Process Benefits

| Feature | Substring Matching (Legacy) | Catalog Hash-Lookup (Current) | Core Benefit |
| :--- | :--- | :--- | :--- |
| **Lookup Time** | `O(N)` (searches all variations) | `O(1)` (direct hash lookup) | Sub-millisecond parsing speed |
| **Duplicate Prevention** | High risk (nested labels) | Zero risk (regex/hash mapping) | High data integrity |
| **Maintenance** | Requires modifying python scripts | Requires modifying dictionary JSON | Code remains untouched when adding new metrics |
| **RAG Precision** | High hallucination rate | Context limited to canonical IDs | Exact numeric context matched for LLMs |

---

## Related Documentation
* [Primary Readme](README.md): Project overview, installation scripts, API reference.
* [System Architecture Spec](docs/architecture/architecture.md): Systems layers overview.
* [Database Schema (Data Dictionary)](docs/features/ingestion/data_dictionary.md): Detailed columns description, indices, and constraints.


</details>

<details>
<summary><b>Troubleshooting Guide & Known Issues (docs/refactoring/troubleshooting.md)</b></summary>

# Troubleshooting Guide and Known Issues

This document details the common troubleshooting steps, pipeline warnings, and historical resolutions for developers working with **QuantumLens**.

For system architecture layouts, see [architecture.md](docs/architecture/architecture.md). For table details, see [data_dictionary.md](docs/features/ingestion/data_dictionary.md).

---

## 1. Ingestion & Pipeline Troubleshooting

| Symptom | Probable Cause | Diagnostic Checklist | Resolution Action |
| :--- | :--- | :--- | :--- |
| **Excel Cell Parse Crash** | Empty, null, or annotated spreadsheet cells parse as `NaN` (Not a Number) in Pandas, which are invalid in PostgreSQL JSONB specifications. | [ ] Check execution logs for `pandas` numeric conversions.<br>[ ] Run the pipeline in dry-run mode and inspect `valued_metrics.json`. | Update sheet preprocessing to handle empty cells using `.replace({np.nan: None})` or similar DataFrame level cleanups in [value_extractor.py](backend/src/ingestion/value_extractor.py). |
| **Missing Period Context** | Column timelines in workbook files use distinct naming conventions (e.g. "Q1 2026" vs "31 March 2026"), causing chronological sorting failures. | [ ] Open sheet row headers and confirm column naming formats.<br>[ ] Print output of `period_mapper.py` to confirm the chronological mapping. | Standardize report timelines to sequential indexes (`period_index: 1`, `period_index: 2`) using [period_mapper.py](backend/src/transformation/period_mapper.py) before loading. |
| **Central KPI Catalog Skip** | The worksheet row labels do not match the exact key entries registered in [metric_dictionary.json](backend/src/ingestion/metric_dictionary.json). | [ ] Look up skipped labels in pipeline execution warnings.<br>[ ] Check if the row label contains leading/trailing whitespaces or numbers. | Add the unrecognized text label mapping to [metric_dictionary.json](backend/src/ingestion/metric_dictionary.json) under lowercase, trimmed constraints. |

---

## 2. Database Connection & Supabase Troubleshooting

| Symptom | Probable Cause | Diagnostic Checklist | Resolution Action |
| :--- | :--- | :--- | :--- |
| **RLS Blocks Ingestion** | The database connection uses the public read-only `anon` API key, and Row Level Security (RLS) blocks anonymous insertions. | [ ] Check variables inside `.env`. Confirm if `SUPABASE_KEY` uses the service role key.<br>[ ] Check Supabase database dashboard console logs. | Update the ETL loader configurations to use the administrative **service role API key** (`SERVICE_ROLE_KEY`) and keep `anon` key for read-only client queries. |
| **Duplicate Database Rows** | Re-running ingestion files attempts to insert duplicate primary rows without checking unique constraints. | [ ] Query metrics group counts: `SELECT metric_id, COUNT(*) FROM metrics GROUP BY metric_id HAVING COUNT(*) > 1`. | Enforce a `UNIQUE` constraint on the `metric_id` column in PostgreSQL and switch to the `.upsert()` function in the Supabase Python client. |

---

## 3. AI & Vector Database Troubleshooting

| Symptom | Probable Cause | Diagnostic Checklist | Resolution Action |
| :--- | :--- | :--- | :--- |
| **Vector DB Path File Errors** | ChromaDB persistent database paths are absolute or reference folders outside the workspace directory structure, causing access blockages. | [ ] Check environment variable `VECTOR_DB_PATH` in `.env`.<br>[ ] Check write access rights for local directories. | Configure `VECTOR_DB_PATH` as a relative path within the repository root (e.g. `src/rag/vector_db`) and clear the local vector DB folder to rebuild index. |
| **High API Query Latency** | SentenceTransformer model (`all-MiniLM-L6-v2`) runs embedding generations on slow CPU hardware instances during boot queries. | [ ] Check API endpoint `/ask` request durations.<br>[ ] Monitor memory (RAM) usage on server boot to identify cold-start bottlenecks. | Cache database texts and vector lists in [embeddings.json](backend/data/generated/embeddings.json) during ETL ingestion, loading pre-computed arrays to ChromaDB on startup. |

---

## Related Documentation
* [Primary Readme](README.md): Project overview, installation scripts, API reference.
* [System Architecture Spec](docs/architecture/architecture.md): Systems layers overview.
* [Database Schema (Data Dictionary)](docs/features/ingestion/data_dictionary.md): Detailed columns description.


</details>

<details>
<summary><b>Detailed Engineering History & Issue Register (docs/refactoring/issues.md)</b></summary>

# Engineering History: Issues, Investigations, and Resolutions

This document records the comprehensive engineering history of QuantumLens. It documents the critical issues encountered during development, the root causes identified, the investigation workflows, the specific code corrections, and the long-term architectural prevention strategies.

---

## Issues Summary Table

| Issue ID | Title | Severity | Category | Affected Component | Date |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **#1** | [JSON Serialization Failure](#1-json-serialization-failure) | High | API / Serialization | `backend/src/transformation/kpi_builder.py` | 2026-01-10 |
| **#2** | [NaN Values Breaking JSON](#2-nan-values-breaking-json) | High | Ingestion / Data Pipeline | `backend/src/ingestion/value_extractor.py` | 2026-01-12 |
| **#3** | [Metric Normalization Problems](#3-metric-normalization-problems) | Medium | Data Transformation | `backend/src/ingestion/metric_extractor.py` | 2026-01-15 |
| **#4** | [Duplicate Database Records](#4-duplicate-database-records) | High | Database Storage | `backend/warehouse/data_loader.py` | 2026-01-18 |
| **#5** | [Supabase Authentication Issues](#5-supabase-authentication-issues) | Critical | Security / Database Connection | `backend/warehouse/supabase_client.py` | 2026-01-20 |
| **#6** | [Datetime UTC Deprecation](#6-datetime-utc-deprecation) | Low | Python Runtime | `backend/src/api/services/record_service.py` | 2026-01-22 |
| **#7** | [KPI Extraction Errors](#7-kpi-extraction-errors) | High | Ingestion / Parser | `backend/src/ingestion/metric_extractor.py` | 2026-01-25 |
| **#8** | [Period Mapping Challenges](#8-period-mapping-challenges) | Medium | Transformation | `backend/src/transformation/period_mapper.py` | 2026-01-28 |
| **#9** | [Excel Ingestion Parsing Issues](#9-excel-ingestion-parsing-issues) | High | Ingestion | `backend/src/ingestion/sheet_scanner.py` | 2026-02-02 |
| **#10** | [ChromaDB Integration](#10-chromadb-integration) | Medium | AI Layer | `backend/src/rag/vector_loader.py` | 2026-02-05 |
| **#11** | [RAG Quality Problems](#11-rag-quality-problems) | High | AI Layer | `backend/src/rag/prompt_builder.py` | 2026-02-08 |
| **#12** | [CORS Deployment Failure](#12-cors-deployment-failure) | Critical | Cloud Deployment | `backend/src/api/main.py` | 2026-02-12 |
| **#13** | [Environment Variable Failures](#13-environment-variable-failures) | High | Configuration | `backend/src/config/settings.py` | 2026-02-15 |
| **#14** | [Vercel Framework Detection](#14-vercel-framework-detection) | Medium | Deployment | Vercel Build | 2026-02-18 |
| **#15** | [Render Deployment Issues](#15-render-deployment-issues) | High | Cloud Deployment | `backend/requirements.txt` | 2026-02-20 |
| **#16** | [Localhost vs Production API](#16-localhost-vs-production-api) | High | Integration | `frontend/services/api.ts` | 2026-02-22 |
| **#17** | [Chart Rendering Problems](#17-chart-rendering-problems) | Medium | Frontend UI | `frontend/components/TimeSeriesChart.tsx` | 2026-02-25 |
| **#18** | [Frontend State Management](#18-frontend-state-management) | Medium | Frontend UI | `frontend/app/dashboard/page.tsx` | 2026-02-28 |
| **#19** | [AI Assistant Development](#19-ai-assistant-development) | Medium | AI Layer | `backend/src/rag/prompt_builder.py` | 2026-03-05 |

---

## 1. JSON Serialization Failure

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | High |
| **Component** | `backend/src/transformation/kpi_builder.py` |
| **Category** | API / Serialization |
| **Date** | 2026-01-10 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | The application threw `TypeError: Object of type Timestamp is not JSON serializable` during ETL runs. All API calls returning metrics crashed with HTTP 500 errors. |
| **Root Cause** | Pandas parses Excel date cells as `pandas.Timestamp` structures. Python's default `json` library lacks serialization schemas for these objects. |
| **Investigation** | Traced the stack trace to the API router conversion layer. confirmed raw timestamp types were passed into Supabase load payloads. |
| **Solution** | Converted all timestamps to ISO-8601 strings using the `.isoformat()` method before serialization. |

### Code Diffs

```diff
# backend/src/transformation/kpi_builder.py
-def format_timestamp(ts):
-    return ts
+def format_timestamp(ts):
+    if hasattr(ts, "isoformat"):
+        return ts.isoformat()
+    return str(ts)
```

### Prevention Strategy
* **Long-Term Rule**: Enforce serialization boundaries at ingestion points.
* **Automation**: Integrated Pydantic schema validation tests that raise warnings during check-ins if raw timestamps are passed.

---

## 2. NaN Values Breaking JSON

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | High |
| **Component** | `backend/src/ingestion/value_extractor.py` |
| **Category** | Ingestion / Data Pipeline |
| **Date** | 2026-01-12 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | FastAPI validations failed, and Supabase client insertions raised SQL exceptions due to invalid JSON tokens (`NaN` instead of `null`). |
| **Root Cause** | Pandas maps empty spreadsheet cells to `numpy.nan` (float NaN). The default Python `json` compiler encodes this as the invalid JSON token `NaN`. |
| **Investigation** | Inspected `mapped_metrics.json` and found raw `NaN` strings. Checked cell types in `value_extractor.py` and found they were parsed as floating-point NaNs. |
| **Solution** | Cleaned cells by converting NumPy float `nan` values to standard Python `None` before database calls. |

### Data Types Comparison Table
| Type | Python Representation | JSON Serialization | SQL Translation | Behavioral Classification |
| :--- | :--- | :--- | :--- | :--- |
| **NaN** | `float('nan')` / `np.nan` | `NaN` (Invalid JSON) | `NaN` (Float only) | Numeric error state (Not-a-Number) |
| **None** | `None` | `null` | `NULL` | Void/absence of a value |
| **NULL** | `None` | `null` | `NULL` | Unallocated database cell |

### Code Diffs

```diff
# backend/src/ingestion/value_extractor.py
-        numeric_values = [
-            value
-            for value in row.get("row_values", [])
-            if isinstance(value, (int, float))
-        ]
+        numeric_values = []
+        for value in row.get("row_values", []):
+            if isinstance(value, (int, float)):
+                if pd.isna(value) or value is np.nan:
+                    numeric_values.append(None)
+                else:
+                    numeric_values.append(float(value))
```

### Prevention Strategy
* **Long-Term Rule**: Clean dataframe matrices using `.replace({np.nan: None})` before mapping dicts.
* **Automation**: Configured structural API tests verifying inputs return valid JSON nulls.

---

## 3. Metric Normalization Problems

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Component** | `backend/src/ingestion/metric_extractor.py` |
| **Category** | Data Transformation |
| **Date** | 2026-01-15 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Identical business indicators loaded under separate entries (e.g. "Total Revenue" vs "Operating Revenue"), breaking historical trend analytics. |
| **Root Cause** | Financial labels fluctuate across sheets. The system used loose substring matching instead of normalized lookup indexes. |
| **Investigation** | Screened Supabase metrics and found duplicated indicators with separate IDs. Checked `metric_extractor.py` and confirmed substring matching was active. |
| **Solution** | Established a centralized `metric_dictionary.json` catalog and converted extraction to constant-time hash lookups on trimmed tokens. |

### Normalization Mapping Table
| Input String Variant | Normalized Token | Assigned Metric ID | Abbreviation | Business Context |
| :--- | :--- | :--- | :--- | :--- |
| "Total Revenue" | `revenue` | 31 | `rev` | Top-line sales |
| "Operating Revenue" | `revenue` | 31 | `rev` | Top-line sales |
| "Net Interest Income"| `net_interest_income`| 1 | `nii` | Banking net yield |

### Code Diffs

```diff
# backend/src/ingestion/metric_extractor.py
-def normalize_name(raw_name):
-    if "interest income" in raw_name.lower():
-        return 1, "net_interest_income"
+def normalize_name(raw_name):
+    clean_token = " ".join(raw_name.lower().split())
+    match = metric_dictionary.get(clean_token)
+    if match:
+        return match["metric_id"], match["normalized_metric_name"]
+    return None, None
```

### Prevention Strategy
* **Long-Term Rule**: Centralize synonyms and aliases in static JSON catalogs.
* **Automation**: Programmed pipeline tests validating that skipped sheet labels raise build-stage warnings.

---

## 4. Duplicate Database Records

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | High |
| **Component** | `backend/warehouse/data_loader.py` |
| **Category** | Database Storage |
| **Date** | 2026-01-18 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Re-executing ETL ingestion files multiplied the database row count, causing duplicate data points for identical periods. |
| **Root Cause** | The database loader used SQL `INSERT` statements without checking unique key constraints. The schema did not enforce constraints on the `metric_id` field. |
| **Investigation** | Audited Supabase metrics group counts. Confirmed database duplicates on identical source workbooks. |
| **Solution** | Altered the Postgres schema to add a `UNIQUE` constraint on `metric_id` and updated loader scripts to perform `.upsert()`. |

### Database Operations Comparison
| Command Pattern | Action on Constraint Conflict | Table Growth Profile | Duplicate Hazard |
| :--- | :--- | :--- | :--- |
| **Insert** | Throws error (with unique key constraint) / appends rows (without constraint). | Exponential | High |
| **Upsert (Current)**| Overwrites existing record columns. | Linear (One row per ID) | None |

### Code Diffs

```diff
# Database migration SQL
-ALTER TABLE metrics ADD COLUMN metric_id INTEGER;
+ALTER TABLE metrics ADD CONSTRAINT unique_metric_id UNIQUE (metric_id);
```
```diff
# backend/warehouse/data_loader.py
-supabase.table("metrics").insert(payload).execute()
+supabase.table("metrics").upsert(payload).execute()
```

### Prevention Strategy
* **Long-Term Rule**: Enforce natural unique key constraints in database architectures.
* **Automation**: Configured integration tests that run ingestion twice and check that the row counts remain constant.

---

## 5. Supabase Authentication Issues

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | Critical |
| **Component** | `backend/warehouse/supabase_client.py` |
| **Category** | Security / Database Connection |
| **Date** | 2026-01-20 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Ingestion pipeline writes failed with `401 Unauthorized` or `403 Forbidden` errors, while local read operations succeeded. |
| **Root Cause** | The pipeline used the public `anon` key. Supabase Row Level Security (RLS) blocked insertions unless authenticated via service credentials. |
| **Investigation** | Inspected `supabase_client.py` keys. Verified RLS logs in the Supabase console, showing blocked insert statements. |
| **Solution** | Updated loader configurations to connect using the administrative Service Role key (`SUPABASE_KEY` / `SERVICE_ROLE_KEY`). |

### API Credentials Access Matrix
| Key Variant | Security Isolation | Allowed Operations | Safe for Frontend? | Bypass RLS? |
| :--- | :--- | :--- | :--- | :--- |
| **Anon Key** | Enforced by policies | SELECT | Yes | No |
| **Service Key**| Enforced at engine level | SELECT, INSERT, UPDATE, DELETE | No (Keep secret) | Yes |

### Code Diffs

```diff
# backend/warehouse/supabase_client.py
-SUPABASE_KEY = os.getenv("SUPABASE_PUBLIC_ANON_KEY")
+SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Administrative Service Key
```

### Prevention Strategy
* **Long-Term Rule**: Isolate administrative ETL connections from public client read APIs.
* **Automation**: Configured CI/CD secrets screening to block hardcoded database service keys.

---

## 6. Datetime UTC Deprecation

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | Low |
| **Component** | `backend/src/api/services/record_service.py` |
| **Category** | Python Runtime |
| **Date** | 2026-01-22 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Console printed startup warnings: `DeprecationWarning: datetime.datetime.utcfromtimestamp() is deprecated`. |
| **Root Cause** | Python 3.13 deprecates naive UTC datetime creation methods because they lack explicit timezone offset indicators. |
| **Investigation** | Traced warnings to timestamp helpers. Found instances of `datetime.utcnow()` and `datetime.utcfromtimestamp()`. |
| **Solution** | Updated creation logic to use timezone-aware UTC datetime objects: `datetime.now(timezone.utc)`. |

### Code Diffs

```diff
# backend/src/api/services/record_service.py
-from datetime import datetime
-return datetime.utcnow().isoformat()
+from datetime import datetime, timezone
+return datetime.now(timezone.utc).isoformat()
```

### Prevention Strategy
* **Long-Term Rule**: Avoid timezone-naive datetime objects.
* **Automation**: Configured unit testing suites to treat Python deprecation warnings as errors, blocking builds containing deprecated datetime calls.

---

## 7. KPI Extraction Errors

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | High |
| **Component** | `backend/src/ingestion/metric_extractor.py` |
| **Category** | Ingestion / Parser |
| **Date** | 2026-01-25 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Parser logged false positives (e.g. matching "Tax on Net Fee Income" as "Net Fee Income") and false negatives. |
| **Root Cause** | The extraction engine relied on loose substring checking, which triggered matches on nested labels. |
| **Investigation** | Audited raw logging files. Found substring checks like `if "fee income" in label` triggered false positives. |
| **Solution** | Updated matching to use exact boundaries and regex logic on lowercase, trimmed string tokens. |

### Extraction Accuracy Comparison
| String Input | Substring Result | Clean Regex Result | Status Classification |
| :--- | :--- | :--- | :--- |
| "Net Fee Income" | Match | Match | Correct Match |
| "Tax on Net Fee Income"| Match | No Match | Avoided False Positive |
| "Fee Income Note" | Match | No Match | Avoided False Positive |

### Code Diffs

```diff
# backend/src/ingestion/metric_extractor.py
-def match_metric(label):
-    if "fee income" in label:
-        return "net_fee_income"
+def match_metric(label):
+    clean_label = label.strip().lower()
+    clean_label = re.sub(r'^(total|net|gross)\s+', '', clean_label)
+    # Enforce boundary checks
+    return exact_lookup(clean_label)
```

### Prevention Strategy
* **Long-Term Rule**: Do not use loose substring checks for semantic categorization.
* **Automation**: Created evaluation datasets of common financial labels to evaluate extractor matching accuracy during builds.

---

## 8. Period Mapping Challenges

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Component** | `backend/src/transformation/period_mapper.py` |
| **Category** | Transformation |
| **Date** | 2026-01-28 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Time-series charts displayed values out of order, and the AI model failed to accurately interpret trend directions because raw metrics lacked explicit date bounds. |
| **Root Cause** | Spreadsheet cells contain numerical arrays without explicit period keys (e.g. `[8945, 9196, 8777]`). The timeline context is often defined separately in top-row header cells, making it difficult to align raw row values. |
| **Investigation** | Audited `valued_metrics.json`. Found data stored as plain arrays without index mappings. Columns in different sheets used different sorting orders. |
| **Solution** | Built `period_mapper.py` to index numeric elements sequentially (`period_index`) and sort arrays chronologically. |

### Period Mapping Schema
```text
Raw Excel Layout:  [Column B: 4Q25] [Column C: 1Q26] [Column D: 2Q26]
                          │               │               │
                          ▼               ▼               ▼
Database JSONB:     [Period ID: 1]  [Period ID: 2]  [Period ID: 3]
```

### Code Diffs

```diff
# backend/src/transformation/period_mapper.py
+def map_periods(numeric_list, chronological=True):
+    mapped = []
+    iterator = enumerate(numeric_list) if chronological else enumerate(reversed(numeric_list))
+    for idx, val in iterator:
+        mapped.append({
+            "period_index": idx + 1,
+            "value": val
+        })
+    return mapped
```

### Prevention Strategy
* **Long-Term Rule**: Convert positional arrays to explicit key-value structures before database storage.
* **Automation**: Integrated chronos-sorting assertions into data loader schemas.

---

## 9. Excel Ingestion Parsing Issues

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | High |
| **Component** | `backend/src/ingestion/sheet_scanner.py` |
| **Category** | Ingestion |
| **Date** | 2026-02-02 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Ingestion pipeline failed on merged title blocks, empty spacing cells, or formulas instead of calculated values. |
| **Root Cause** | Corporate sheets use layout formats optimized for human readers (merged columns, formula paths), which break standard loaders. |
| **Investigation** | Debugged file reads. Verified merged headers returned `NaN` values for all but the first cell. Formulas imported raw equations like `"=SUM(B12)"`. |
| **Solution** | Switched openpyxl configuration to resolve calculations (`data_only=True`) and implemented forward-fill logic for merged fields. |

### Excel Layout Parsing Matrix
| Cell State | Raw Pandas Result | Clean Ingestion Result | Process Action |
| :--- | :--- | :--- | :--- |
| **Merged Title** | `["Revenue", NaN, NaN]` | `["Revenue", "Revenue", "Revenue"]` | Forward-fill cells |
| **Formula Cell** | `"=SUM(B5:B7)"` | `12450.0` | Read calculated values |
| **Empty Spacing Row**| `[NaN, NaN, NaN]` | Skip Row | Filter null rows |

### Code Diffs

```diff
# backend/src/ingestion/sheet_scanner.py
-wb = openpyxl.load_workbook(file_path)
+wb = openpyxl.load_workbook(file_path, data_only=True)
# Add merged cell forward-filling
+def forward_fill_merged(row):
+    # Forward-fill logic
```

### Prevention Strategy
* **Long-Term Rule**: Parse calculated cell values instead of formula strings.
* **Automation**: Configured pipeline checks to trigger errors if formula indicators are detected in database payloads.

---

## 10. ChromaDB Integration

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Component** | `backend/src/rag/vector_loader.py` |
| **Category** | AI Layer |
| **Date** | 2026-02-05 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Semantic search returned empty results or failed with folder access blockages on startup, and embedding calculations delayed system boot times. |
| **Root Cause** | ChromaDB persistent database paths were misconfigured, and the system regenerated all vector embeddings on every startup instead of loading cached indices. |
| **Investigation** | Inspected `quantumlens.log`. Found database directory initialized outside workspace. Startup benchmarks recorded 45s cold starts due to embedding calculations. |
| **Solution** | Configured a persistent local directory in `settings.py`, and saved pre-computed embeddings to `embeddings.json` during ingestion. |

### Database Connection Schema
```text
ETL Loader ──► [Embeddings JSON Cache] ──► [Local ChromaDB Client] ──► Query Engine
                                                    ▲
                                                    │ Persistence Target
                                           [src/rag/vector_db]
```

### Code Diffs

```diff
# backend/src/rag/vector_loader.py
-client = chromadb.Client()
+client = chromadb.PersistentClient(path=str(settings.VECTOR_DB_PATH))
```

### Prevention Strategy
* **Long-Term Rule**: Cache vector embeddings to avoid expensive runtime recalculations.
* **Automation**: Configured a boot check verifying vector collection presence before routers bind.

---

## 11. RAG Quality Problems

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | High |
| **Component** | `backend/src/rag/prompt_builder.py` |
| **Category** | AI Layer |
| **Date** | 2026-02-08 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | AI assistant returned incorrect numbers, cited unrelated sheets, or exceeded LLM token window limits. |
| **Root Cause** | Cosine similarity thresholds were loose, causing unrelated metrics to dilute prompt context windows. |
| **Investigation** | Audited raw prompts sent to Groq. Found unstructured text dumps that confused the LLM. |
| **Solution** | Refactored context generation to structured key-value configurations and set strict cosine distance thresholds. |

### Code Diffs

```diff
# backend/src/rag/prompt_builder.py
-def build_prompt(question, documents):
-    return f"Context: {documents} Question: {question}"
+def build_prompt(question, retrieved_docs):
+    context = ""
+    for doc in retrieved_docs:
+        context += f"Metric: {doc['metric_name']}\nValues: {doc['values']}\nSource: {doc['sheet']}\n\n"
+    return f"Context:\n{context}\nQuestion: {question}"
```

### Prevention Strategy
* **Long-Term Rule**: Structure RAG prompts as clean key-value records rather than raw string dumps.
* **Automation**: Implemented automated RAG evaluation scripts measuring response accuracy.

---

## 12. CORS Deployment Failure

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | Critical |
| **Component** | `backend/src/api/main.py` |
| **Category** | Cloud Deployment |
| **Date** | 2026-02-12 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Frontend dashboard failed to load API data. Browser console logged CORS access violations. |
| **Root Cause** | FastAPI CORS middleware origins were restricted to `localhost`, blocking deployed Vercel domain preflight checks. |
| **Investigation** | Audited network requests in browser developer tools. Verified API calls were blocked during CORS preflight checks. |
| **Solution** | Added the production Vercel frontend URL to the whitelisted origins array in FastAPI. |

### Code Diffs

```diff
# backend/src/api/main.py
 app.add_middleware(
     CORSMiddleware,
     allow_origins=[
         "http://localhost:3000",
+        "https://quantumlens-hsbc.vercel.app",
     ],
```

### Prevention Strategy
* **Long-Term Rule**: Configure CORS whitelists for all target environments.
* **Automation**: Programmed URL verification checks to run during CI deployment pipelines.

---

## 13. Environment Variable Failures

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | High |
| **Component** | `backend/src/config/settings.py` |
| **Category** | Configuration |
| **Date** | 2026-02-15 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Server failed to start or crashed on DB query loops, raising KeyError warnings for missing environment variables. |
| **Root Cause** | Env variables were not loaded in local shells or configured in cloud hosting panels. |
| **Investigation** | Inspected Render startup logs. Confirmed `os.getenv` returned `None` for database endpoints. |
| **Solution** | Integrated `python-dotenv` into settings initialization and added fallback settings to prevent crashes. |

### Code Diffs

```diff
# backend/src/config/settings.py
+from dotenv import load_dotenv
+load_dotenv()
 class Settings:
-    SUPABASE_URL = os.environ["SUPABASE_URL"]
+    SUPABASE_URL = os.getenv("SUPABASE_URL")
+    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "src/rag/vector_db")
```

### Prevention Strategy
* **Long-Term Rule**: Enforce fail-fast checks for critical variables on startup.
* **Automation**: Configured validation scripts to check required environment configurations on server boot.

---

## 14. Vercel Framework Detection

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Component** | Vercel Build |
| **Category** | Deployment |
| **Date** | 2026-02-18 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Vercel build failed, trying to run compiler routines on the backend instead of the frontend. |
| **Root Cause** | The repository is a monorepo. Vercel scanned the root folder instead of the `frontend` subfolder. |
| **Investigation** | Inspected Vercel console build logs. Confirmed the build was searching for `package.json` at the root. |
| **Solution** | Configured Vercel settings to specify `frontend/` as the root directory of the application. |

### Project Directory Layout
```text
Root folder (quantumlens-HSBC)
 ├── backend/ (Python API)
 └── frontend/ (Next.js App) ◄── Configure as Vercel build target root
```

### Prevention Strategy
* **Long-Term Rule**: Configure build directory targets when using monorepo setups.
* **Automation**: Added a `vercel.json` routing configuration to the repository root.

---

## 15. Render Deployment Issues

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | High |
| **Component** | `backend/requirements.txt` |
| **Category** | Cloud Deployment |
| **Date** | 2026-02-20 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Render builds failed with `ModuleNotFoundError` or crashed with Out of Memory (OOM) errors during startup. |
| **Root Cause** | Production hosting dependencies (`uvicorn`, `gunicorn`) were missing. SentenceTransformers calculations exceeded Render's RAM allocations. |
| **Investigation** | Reviewed build failures in the Render dashboard. Confirmed OOM exceptions during model initialization. |
| **Solution** | Added missing packages to `requirements.txt` and switched to a lightweight model (`all-MiniLM-L6-v2`) to reduce RAM usage. |

### Code Diffs

```diff
# backend/requirements.txt
+uvicorn==0.49.0
+gunicorn==21.2.0
+sentence-transformers==5.6.0
```

### Prevention Strategy
* **Long-Term Rule**: Test model memory usage on lower-tier host specs before production deployment.
* **Automation**: Configured Docker resource limits to simulate production constraints during local testing.

---

## 16. Localhost vs Production API

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | High |
| **Component** | `frontend/services/api.ts` |
| **Category** | Integration |
| **Date** | 2026-02-22 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Deployed Next.js portal loaded correctly but failed to fetch data, attempting to send requests to `http://127.0.0.1:8000`. |
| **Root Cause** | The backend API endpoint was hardcoded to `127.0.0.1:8000` in frontend Axios settings. |
| **Investigation** | Inspected browser network logs. Confirmed request routing was sending queries to localhost. |
| **Solution** | Replaced hardcoded URL strings with environment variable bindings: `process.env.NEXT_PUBLIC_API_URL`. |

### Code Diffs

```diff
# frontend/services/api.ts
-const api = axios.create({ baseURL: 'http://localhost:8000' });
+const api = axios.create({
+  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
+});
```

### Prevention Strategy
* **Long-Term Rule**: Use environment variables to configure URLs across development environments.
* **Automation**: Added build checks that fail compile steps if localhost URLs are detected in source code files.

---

## 17. Chart Rendering Problems

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Component** | `frontend/components/TimeSeriesChart.tsx` |
| **Category** | Frontend UI |
| **Date** | 2026-02-25 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | Time-series charts rendered empty lines or sorted quarters out of order. |
| **Root Cause** | Recharts expected sorted coordinate arrays, but the API returned unsorted JSON metrics containing metadata. |
| **Investigation** | Logged API JSON payloads on the frontend. Confirmed that time-series arrays were unsorted. |
| **Solution** | Implemented client-side chronological sorting by period index before passing data to Recharts. |

### Code Diffs

```diff
# frontend/components/TimeSeriesChart.tsx
+const prepareChartData = (periodValues: any[]) => {
+  return periodValues
+    .map(item => ({
+      name: `Period ${item.period_index}`,
+      value: item.value
+    }))
+    .sort((a, b) => a.name.localeCompare(b.name));
+};
```

### Prevention Strategy
* **Long-Term Rule**: Standardize data shapes on the API level before sending them to the client.
* **Automation**: Added unit tests to verify chart component stability against unsorted datasets.

---

## 18. Frontend State Management

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Component** | `frontend/app/dashboard/page.tsx` |
| **Category** | Frontend UI |
| **Date** | 2026-02-28 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | The dashboard experienced performance lag, and selected filter states reset unexpectedly during panel transitions. |
| **Root Cause** | The dashboard page used a single monolithic state object, which forced full-page re-renders on minor filter adjustments. |
| **Investigation** | Ran React developer profiles. Confirmed that minor chart updates triggered re-renders across all dashboard components. |
| **Solution** | Decoupled state management by splitting the monolithic state object into focused hooks (`selectedMetric`, `selectedRecord`, `searchQuery`). |

### Code Diffs

```diff
# frontend/app/dashboard/page.tsx
-const [state, setState] = useState({ metric: null, record: null, query: "" });
+const [selectedMetric, setSelectedMetric] = useState<number | null>(null);
+const [selectedRecord, setSelectedRecord] = useState<any | null>(null);
+const [searchQuery, setSearchQuery] = useState<string>("");
```

### Prevention Strategy
* **Long-Term Rule**: Keep React state close to the components that use it to avoid redundant rendering.
* **Automation**: Configured page profiling targets to alert on component re-render counts during development.

---

## 19. AI Assistant Development

### Issue Diagnostics

| Attribute | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Component** | `backend/src/rag/prompt_builder.py` |
| **Category** | AI Layer |
| **Date** | 2026-03-05 |

| Phase | Details |
| :--- | :--- |
| **Symptom** | The AI assistant generated overly verbose responses, failed to cite data sources, and hallucinated calculations. |
| **Root Cause** | The system prompt lacked explicit rules and guidelines to constrain the model's behavior. |
| **Investigation** | Checked prompt completions. Confirmed the LLM was using pre-trained knowledge instead of the retrieved context. |
| **Solution** | Refactored system prompts to define the model's role as a financial analyst and added constraints requiring source citations. |

### Code Diffs

```diff
# backend/src/rag/prompt_builder.py
-    return f"Answer: {question} using {retrieved_docs}"
+    return f"""You are a financial analyst copilot.
+    Rules:
+    1. Restrict your answer strictly to the context below.
+    2. Quote exact numbers and sources.
+    3. If context is insufficient, state that the data is not available.
+    Context: {retrieved_docs} Question: {question}"""
```

### Prevention Strategy
* **Long-Term Rule**: Constrain RAG prompts with strict context guidelines to prevent hallucinations.
* **Automation**: Added evaluation query test lists to assess citation and answer accuracy during updates.


</details>

<details>
<summary><b>FastAPI Backend Server Documentation (backend/README.md)</b></summary>

# FastAPI Backend Server (backend/)

This is the backend REST API engine for the **QuantumLens** platform. It handles Excel data ingestion pipelines, manages the dual-database warehouses, generates semantic vector embeddings, and hosts the multi-agent AI copilot.

For general details on the project architecture or dashboards, see the root [README.md](README.md).

---

## Technical Stack & Configuration

| Module | Technology | Role |
| :--- | :--- | :--- |
| **Routing & Core** | FastAPI + Uvicorn | High-performance ASGI REST endpoints. |
| **Tabular Parser** | Pandas + openpyxl | Traverses sheets, extracts values, and cleans NaN anomalies. |
| **AI Embeddings** | SentenceTransformers | Local 384-dimensional dense vector generations (`all-MiniLM-L6-v2`). |
| **Vector Database**| ChromaDB | Zero-config, persistent local vector indexing. |
| **LLM Inference** | Groq Cloud Client | Context-grounded response generation via Llama-3.3. |

---

## Systems Architecture Diagram

```mermaid
graph TD
    %% Define Nodes
    FastAPI["FastAPI Web Router (src/api/)"]
    
    subgraph ETLPipeline ["ETL Pipeline (src/ingestion/ & src/transformation/)"]
        Reader["Workbook Reader"]
        Scanner["Sheet Scanner"]
        Extractor["Metric Extractor"]
        Mapper["Period Mapper"]
        Builder["KPI Builder"]
    end
    
    subgraph DatabaseLayer ["Database Warehouse Layer (warehouse/)"]
        Supabase[("Supabase (PostgreSQL)<br>[Production JSONB arrays]")]
        Oracle[("Oracle Database 19c<br>[Relational Period rows]")]
    end

    subgraph AIEngine ["AI & Semantic RAG Layer (src/rag/ & src/agents/)"]
        Chroma[("ChromaDB Vector Store<br>[Local Index Cache]")]
        Planner["Planner Agent"]
        SQLAgent["SQL Agent"]
        RAGAgent["RAG Agent"]
    end

    %% Connections
    FastAPI <-->|SQL Queries| Supabase
    FastAPI <-->|Query Context| Chroma
    
    %% ETL Ingestion Flow
    xlsx["Raw XLSX Files"] --> Reader
    Reader --> Scanner
    Scanner --> Extractor
    Extractor --> Mapper
    Mapper --> Builder
    Builder -->|Batch Upserts| Supabase
    Builder -->|Insert Rows| Oracle
    
    %% Vector Ingestion Flow
    Supabase -->|SQL Extract| Chroma
    
    %% Multi-Agent Flow
    FastAPI <-->|Natural Query| Planner
    Planner <-->|Intent Matrix| SQLAgent
    Planner <-->|Intent Matrix| RAGAgent
    SQLAgent <--> Oracle
    RAGAgent <--> Chroma
```

---

## Dual-Database Warehouse Layouts

The database layer processes data into two distinct target topologies:

### 1. Supabase (PostgreSQL 15) Table: `metrics`
Stores complete time-series observations inside a single row using a dynamic JSONB array column.
* **Primary Key**: `id` (SERIAL)
* **Unique Constraint**: `metric_id` (enforces 1 row per KPI)
* **Time-Series Column**: `period_values` (JSONB)
* **Index**: B-Tree indices on `id`, `metric_id`, and `metric_name`

### 2. Oracle Database Table: `metrics`
Flattens observations into individual rows (one row per quarter/period) for OLAP reports.
* **Primary Key**: `id` (NUMBER GENERATED ALWAYS AS IDENTITY)
* **Chronological Columns**: `period` (VARCHAR2) & `value` (NUMBER)
* **Classification Columns**: `category` (VARCHAR2), `unit` (VARCHAR2)

---

## Local Ingestion and API Setup

### Prerequisites Checklist
- [ ] Python 3.13+ installed.
- [ ] SQLite3 and local system path configurations enabled.
- [ ] Oracle Client libraries (instant client) configured for python environment connections.

### Setup and execution commands

| Step | Action | Command | Notes |
| :--- | :--- | :--- | :--- |
| **1** | Create Virtual Env | `python -m venv .venv` | Creates sandbox environment. |
| **2** | Activate Env (Win) | `.venv\Scripts\Activate.ps1` | Activates powershell environment. |
| **3** | Activate Env (Unix)| `source .venv/bin/activate` | Activates bash environment. |
| **4** | Install Requirements | `pip install -r requirements.txt` | Installs Pandas, FastAPI, ChromaDB, Uvicorn. |
| **5** | Configure Environment | `copy .env.example .env` | Duplicate config file and inject credentials. |
| **6** | Run Ingestion Pipeline| `python src/ingestion/sheet_scanner.py` | Traverses XLSX data and structures raw records. |
| **7** | Load Database | `python warehouse/data_loader.py` | Batches metrics payload to Supabase metrics table. |
| **8** | Load Oracle Warehouse | `python warehouse/load_to_oracle.py` | Flattens observations and inserts records to Oracle. |
| **9** | Launch REST API | `uvicorn src.api.main:app --reload --port 8000` | Boots API server on port 8000 with hot-reload. |

---

## Environment Variables Configuration

> [!WARNING]
> - Never commit the `.env` file containing actual secrets to public repositories.
> - Ensure all variables are configured in the cloud host panel during deployments.

| Variable Name | Required | Description | Default Local |
| :--- | :--- | :--- | :--- |
| `SUPABASE_URL` | YES | Endpoint for Supabase Database REST interface. | `https://<YOUR_PROJECT_ID>.supabase.co` |
| `SUPABASE_KEY` | YES | Service Role administrative key to bypass RLS policies. | `<YOUR_SUPABASE_SERVICE_ROLE_KEY>` |
| `GROQ_API_KEY` | YES | API token for Groq Cloud LLM completions. | `<YOUR_GROQ_API_KEY>` |
| `VECTOR_DB_PATH` | NO | Local directory to persist ChromaDB index assets. | `src/rag/vector_db` |
| `EMBEDDINGS_PATH`| NO | Local file path caching pre-computed embeddings. | `data/generated/embeddings.json` |
| `EMBEDDING_MODEL`| NO | HuggingFace embedding model ID. | `sentence-transformers/all-MiniLM-L6-v2` |
| `TOP_K` | NO | Top document count returned during semantic search retrieval. | `5` |

---

## API Endpoints Reference

### Endpoints Matrix
| Method | Route | Description | Request Body (JSON) | Success Code |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Verify API server connectivity | None | `200 OK` |
| `GET` | `/health` | Ingestion status check | None | `200 OK` |
| `GET` | `/metrics` | Retrieve list of unique metrics | None | `200 OK` |
| `GET` | `/metric/{metric_id}`| Retrieve occurrences of a specific metric ID | None (Path Parameter) | `200 OK` |
| `GET` | `/record/{record_id}`| Retrieve metric row and timeline values by ID | None (Path Parameter) | `200 OK` |
| `POST` | `/search` | Query vector space for semantic similarity | `{"query": "...", "top_k": 3}`| `200 OK` |
| `POST` | `/ask` | Execute full multi-agent RAG reasoning | `{"question": "..."}` | `200 OK` |

---

### Request/Response JSON Formats

#### POST `/ask`

##### Request JSON Structure
```json
{
  "question": "Why did Expected Credit Losses (ECL) rise?"
}
```

##### Response JSON Structure
```json
{
  "question": "Why did Expected Credit Losses (ECL) rise?",
  "answer": "- According to sheet 'Group Income Statement' in '260505-1q-2026-data-pack-excel.xlsx':\n- Expected Credit Losses (ECL) rose due to fraud-related exposure on UK securitisation transactions and rising Middle East geopolitical volatility.",
  "sources": [
    {
      "metric_id": 5,
      "metric_name": "expected_credit_losses",
      "sheet_name": "Group Income Statement",
      "source_workbook": "260505-1q-2026-data-pack-excel.xlsx",
      "row_number": 12
    }
  ]
}
```

---

## Related Documentation
* [Primary Readme](README.md): Project overview and complete monorepo details.
* [Frontend Readme](frontend/README.md): Next.js dashboard visual portal instructions.
* [System Architecture Spec](docs/architecture/architecture.md): Systems layers and sequence flows.


</details>

<details>
<summary><b>Frontend Analytics Portal Documentation (frontend/README.md)</b></summary>

# Next.js Analytics Portal (frontend/)

This is the interactive client dashboard for the **QuantumLens** financial intelligence platform. It provides a visual interface for executive strategy, risk observation, and natural language reasoning (AI financial assistant).

For general backend endpoints, models, or database queries, see the [backend/README.md](backend/README.md).

---

## Technical Stack & Visual Framework

| Layer | Selected Package | Purpose |
| :--- | :--- | :--- |
| **Framework** | Next.js 15+ (App Router) | Core layouts routing and server components. |
| **UI Components** | React 19+ | Dynamic component rendering and hooks state. |
| **Style System** | TailwindCSS 3.4+ | CSS layouts, utility spacing, and theme variables. |
| **Data Graphs** | Recharts / Chart.js | Visual rendering of time-series trend lines. |
| **HTTP Client** | Axios / Fetch | API requests routing to backend routers. |

---

## Interactive Dashboard Views

The Next.js client organizes analytics into five strategic "War Rooms":

### Dashboard 1: Global Banking Pulse
* **Core Metrics**: Net Interest Income (NII), CET1 capital ratio, Return on Tangible Equity (RoTE), liquidity levels, and loan growth rates.
* **Interactivity**: Dynamic regional heatmaps, timeline cross-filtering, and animated trend transitions.

### Dashboard 2: Wealth Migration Observatory
* **Core Metrics**: Asia wealth inflows ($34B in Q1 2026), net new wealth assets ($39B net new money), insurance growth, and HNW capital concentration.
* **Interactivity**: Capital concentration charts and deposit migration flow trackers.

### Dashboard 3: Credit Stress Radar
* **Core Metrics**: Expected Credit Losses (ECL) trends (guidance raised to 45bps), sector-level write-off ratios, and UK securitisation fraud warnings.
* **Interactivity**: Stress scenario models visualizing asset risk propagation under macroeconomic shocks.

### Dashboard 4: Strategic Transformation Tracker
* **Core Metrics**: Asset disposals, simplification cost savings targets ($1.5B), Hang Seng privatization synergies ($0.5B), and capital reallocation programs.
* **Interactivity**: Milestone checklist meters and operational budget analytics charts.

### Dashboard 5: Banking Contagion Network
* **Core Metrics**: Relational risk propagation maps pulling from Neo4j (Middle East Conflict ──► Energy Price Volatility ──► Expected Credit Losses ──► Capital Deterioration).
* **Interactivity**: Interactive node graph visualization showing asset exposure and liquidity dependencies.

---

## Getting Started

### Prerequisites Checklist
- [ ] Node.js version 18.x or later installed.
- [ ] Running instance of the FastAPI backend server.

### Local Development Setup

| Step | Action | Shell Command | Notes |
| :--- | :--- | :--- | :--- |
| **1** | Restore NPM Modules | `npm install` | Restores React, Tailwind, Recharts, and Axios. |
| **2** | Configure Local Env | `copy .env.example .env.local` | Binds public API URL. |
| **3** | Launch Local Host | `npm run dev` | Spins up dev server on [http://localhost:3000](http://localhost:3000). |
| **4** | Compile Build | `npm run build` | Optimizes assets and compiles static paths. |
| **5** | Run Production Mode | `npm run start` | Serves compiled output files. |

---

## Environment Variables Configuration

> [!WARNING]
> Do not commit `.env.local` containing actual backend production URLs. Keep configurations restricted to local variables.

| Variable Name | Environment | Description | Default Local |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Client Runtime | HTTP address pointing to the FastAPI backend API server. | `http://localhost:8000` |

---

## Production Deployment (Vercel)

Vercel is the recommended hosting platform for Next.jsApp Router portals. Follow these steps:

| Step | Phase | Vercel Panel Configuration |
| :--- | :--- | :--- |
| **1** | **Import Project** | Connect your GitHub repository to Vercel. |
| **2** | **Root Directory** | Configure directory target override: `frontend` |
| **3** | **Build Commands** | Framework preset: **Next.js**. Keep standard build parameters. |
| **4** | **Environment Variables**| Add `NEXT_PUBLIC_API_URL` pointing to your deployed Render backend API. |
| **5** | **Deploy** | Click **Deploy** to compile Next.js static pages. |

---

## Related Documentation
* [Primary Readme](README.md): Complete repository layouts.
* [Backend Readme](backend/README.md): FastAPI REST routing specs.
* [System Architecture Spec](docs/architecture/architecture.md): Systems layers overview.


</details>
