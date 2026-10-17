<!-- -------------------------------------------------------------------
Copyright (c) 2026 Ved Vivek Talmaley. All Rights Reserved.
This project and its source code are strictly proprietary.
Unauthorized copying, distribution, or use is strictly prohibited.
------------------------------------------------------------------- -->

# System Architecture Specification — Version 10.0.0

This document details the architectural layout, system layers, and component interactions of **QuantumLens** (also known as *HSBC Atlas* or *Project Basilisk*), an institutional-grade banking intelligence platform for HSBC Q1 2026 reporting.

For a high-level overview, deployment metrics, or setup instructions, see the primary [README.md](../../README.md). For frontend dashboard details, see [frontend/README.md](../../frontend/README.md). For backend services, see [backend/README.md](../../backend/README.md).

---

## 6-Layer Architecture Overview

QuantumLens is built on six decoupled engineering layers. This decoupling ensures that dense vector embeddings, LLM reasoning, and database warehouse operations run reliably with zero circular dependencies.

```mermaid
graph TD
    %% Define Nodes
    subgraph ClientLayer ["Layer 5: Executive Analytics Dashboard (frontend/)"]
        UI["Next.js 16 + React 19 UI<br>(KPIs, Variance Tables, Multi-Charts, AI Analyst)"]
    end

    subgraph APILayer ["Layer 6: AI Copilot Router (backend/src/api/)"]
        FastAPI["FastAPI Web Router<br>(/metrics, /record, /ask, /search)"]
    end

    subgraph MicroserviceLayer ["Microservice Layer (services/embedding-service/)"]
        EmbedSvc["Embedding Microservice (:8001)<br>(all-MiniLM-L6-v2 on CPU)"]
    end

    subgraph AILayer ["Layer 3: AI Intelligence & Vector Search (backend/src/rag/)"]
        Chroma[("ChromaDB Vector Store<br>[financial_documents collection]")]
        Retriever["DocumentRetriever<br>(HTTP embed via microservice)"]
        Groq["Groq Cloud API<br>(llama-3.3-70b-versatile)"]
    end

    subgraph OrchestrationLayer ["Multi-Agent Orchestration (backend/src/agents/)"]
        Planner["Planner Agent"]
        SQLAgent["SQL Agent"]
        RAGAgent["RAG Agent"]
        Auditor["Data Auditor Agent"]
        RespAgent["Response Agent"]
    end

    subgraph DataEngineering ["Layer 1: Data Engineering Pipeline (backend/src/ingestion/)"]
        CanonicalJSON["Canonical mapped_metrics.json<br>(456 records, 90 PBT rows)"]
        DataLoader["Supabase Data Loader<br>(Automated Backup & Upsert)"]
    end

    subgraph StorageLayer ["Database Warehouse Layer (backend/warehouse/)"]
        Supabase[("Supabase (PostgreSQL 15)<br>[456 Verified Canonical Records]")]
        Backups[("Automated JSON Backups<br>[data/backups/]")]
    end

    %% Define Connections
    UI <-->|HTTP REST :8000| FastAPI
    FastAPI <-->|SQL Queries| Supabase
    FastAPI <-->|Orchestrate Query| Planner
    
    Planner --> SQLAgent
    Planner --> RAGAgent
    SQLAgent <--> Supabase
    RAGAgent --> Retriever
    
    Retriever <-->|POST /embed :8001| EmbedSvc
    Retriever <-->|Cosine Distance Query| Chroma
    
    Planner --> Auditor
    Auditor --> RespAgent
    RespAgent <-->|Context + Prompt| Groq
    
    DataLoader --> Backups
    DataLoader -->|Batch Upsert| Supabase
    CanonicalJSON --> DataLoader

    %% Styles
    classDef client fill:#0f172a,stroke:#334155,stroke-width:2px,color:#fff;
    classDef api fill:#1e293b,stroke:#475569,stroke-width:2px,color:#fff;
    classDef embed fill:#3b82f6,stroke:#1d4ed8,stroke-width:2px,color:#fff;
    classDef storage fill:#334155,stroke:#64748b,stroke-width:2px,color:#fff;
    classDef ai fill:#e11d48,stroke:#9f1239,stroke-width:2px,color:#fff;
    classDef etl fill:#d97706,stroke:#b45309,stroke-width:2px,color:#fff;

    class UI client;
    class FastAPI api;
    class EmbedSvc embed;
    class Supabase,Backups,Chroma storage;
    class Retriever,Groq,Planner,SQLAgent,RAGAgent,Auditor,RespAgent ai;
    class CanonicalJSON,DataLoader etl;
```

---

## Technical Layers Matrix

| Layer | Responsibility | Input Shape | Output Shape | Data Store Target |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1: Pipeline** | Validating canonical financial records and executing natural key upserts. | Raw Excel files (`.xlsx`) / canonical JSON | Cleaned 456 JSON metric coordinates | Supabase / Automated Backups |
| **Layer 2: Graph** | Modeling counterparty risk, wealth flows, and systemic contagion paths (Roadmap). | Structured KPI metrics | Entity node networks and exposures | Neo4j Graph DB |
| **Layer 3: NLP & Vectors** | Generating 384-dimensional dense vectors via microservice and querying ChromaDB. | User query strings | Top-k contextual financial passages | ChromaDB Vector Store |
| **Layer 4: Forecasting** | Modeling macro rate scenarios on NII and deposit migration (Roadmap). | Relational metrics history | Predictive timeline indicators | Warehouse databases |
| **Layer 5: UI Portal** | Executive war-room dashboard with statement tables, variance analysis, and charts. | REST responses, user interactions | Interactive financial tables & charts | Next.js 16 (Vercel) |
| **Layer 6: AI Copilot** | Multi-agent orchestrated reasoning combining SQL metrics with semantic search documents. | Natural language questions | Factual, source-attributed financial replies | FastAPI (Render / Docker) |

---

## Modular System Breakdown

| Script / Module | Architecture Layer | Core Function | Primary Python Packages | File Path |
| :--- | :--- | :--- | :--- | :--- |
| **data_loader.py** | Layer 1: Data Pipeline | Validates canonical metrics, creates backup snapshot, and upserts to Supabase. | `supabase`, `argparse`, `json` | [data_loader.py](../../backend/warehouse/data_loader.py) |
| **supabase_client.py** | Layer 1: Data Pipeline | Manages lazy singleton client connection to Supabase PostgreSQL warehouse. | `supabase`, `dotenv` | [supabase_client.py](../../backend/warehouse/supabase_client.py) |
| **query_service.py** | Layer 6: AI Copilot | Metric alias resolution (PBT, CET1, NII) and sorted sheet querying. | `supabase` | [query_service.py](../../backend/warehouse/query_service.py) |
| **document_retriever.py**| Layer 3: AI Intelligence | Routes query embedding requests to microservice and queries local ChromaDB. | `chromadb`, `urllib.request` | [document_retriever.py](../../backend/src/rag/document_retriever.py) |
| **app.py (Embedding)** | Microservice Layer | Standalone FastAPI microservice generating sentence embeddings via PyTorch CPU. | `fastapi`, `sentence-transformers` | [app.py](../../services/embedding-service/app.py) |
| **orchestrator.py** | Layer 6: AI Copilot | Multi-agent execution loop with memory resolution, planning, and auditing. | Internal agent framework | [orchestrator.py](../../backend/src/agents/orchestrator.py) |
| **planner.py** | Layer 6: AI Copilot | Analyzes user question and produces multi-step execution plans. | Internal agent framework | [planner.py](../../backend/src/agents/planner.py) |
| **llm_service.py** | Layer 6: AI Copilot | Context-grounded LLM answer generation with lazy Groq client initialization. | `groq` | [llm_service.py](../../backend/src/rag/llm_service.py) |
| **main.py** | Layer 6: REST API | Root FastAPI application mounting routers for metrics, records, RAG, and health. | `fastapi`, `uvicorn` | [main.py](../../backend/src/api/main.py) |

---

## Multi-Agent RAG Query Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as Executive / Analyst
    participant UI as Next.js Dashboard
    participant API as FastAPI Router (/ask)
    participant Orchestrator as Agent Orchestrator
    participant Retriever as DocumentRetriever
    participant EmbedSvc as Embedding Microservice (:8001)
    participant Chroma as ChromaDB Vector Store
    participant Warehouse as Supabase Warehouse
    participant LLM as Groq Cloud API

    User->>UI: Selects prompt pill / types inquiry
    UI->>API: POST /ask { "question": "What is PBT?" }
    activate API
    API->>Orchestrator: execute(question)
    activate Orchestrator
    
    Orchestrator->>Warehouse: Query canonical metric data (metric_id=7)
    Warehouse-->>Orchestrator: Return PBT observations ($9,376M, Row 13)
    
    Orchestrator->>Retriever: retrieve(question, top_k=3)
    activate Retriever
    Retriever->>EmbedSvc: POST /embed { "texts": [question] }
    activate EmbedSvc
    EmbedSvc-->>Retriever: { "embeddings": [[...384 float vector...]] }
    deactivate EmbedSvc
    
    Retriever->>Chroma: query(query_embeddings, n_results=3)
    Chroma-->>Retriever: Document passages (Earnings Release p.34, p.46)
    Retriever-->>Orchestrator: Formatted document context
    deactivate Retriever
    
    Orchestrator->>LLM: Generate synthesis (Prompt + Metrics + Vector Docs)
    activate LLM
    LLM-->>Orchestrator: Context-grounded financial analysis
    deactivate LLM
    
    Orchestrator-->>API: Synthesized financial response
    deactivate Orchestrator
    API-->>UI: HTTP 200 OK JSON { answer, sources }
    deactivate API
    UI-->>User: Renders key findings, citations, and latency
```

---

## Canonical Data Verification Matrix

| Verification Target | Expected Standard | Observed Production Status |
| :--- | :--- | :--- |
| **Total Metric Records** | 456 rows | **456 rows verified in Supabase** |
| **Profit Before Tax (PBT)** | 90 rows across business segments | **90 rows verified active** |
| **CET1 Capital & Ratio** | Full capital adequacy notes | **Verified in balance sheet & schedules** |
| **Net Interest Income (NII)** | 3 group observations | **Verified in group income statement** |
| **Database Conflict Key** | `metric_id, sheet_name, row_number` | **Enforced via Supabase unique index** |
| **Automated Backups** | Timestamped JSON before load | **Persisted in `backend/data/backups/`** |

---

## Proprietary License Notice

> **Copyright © 2026 Ved Vivek Talmaley. All Rights Reserved.**  
> *This project and its original source code are strictly proprietary. Unauthorized copying, modification, distribution, or reproduction of this repository, via any medium, is strictly prohibited.*
