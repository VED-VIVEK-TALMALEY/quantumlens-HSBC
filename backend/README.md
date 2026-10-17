<!-- -------------------------------------------------------------------
Copyright (c) 2026 Ved Vivek Talmaley. All Rights Reserved.
This project and its source code are strictly proprietary.
Unauthorized copying, distribution, or use is strictly prohibited.
------------------------------------------------------------------- -->

# FastAPI Backend & Intelligence Services (backend/) — Version 10.0.0

This is the backend REST API engine and data intelligence core for the **QuantumLens** platform. It provides high-performance financial endpoints, orchestrates multi-agent financial reasoning, interfaces with the canonical Supabase metrics warehouse, and queries semantic document embeddings.

For client dashboard details, see [frontend/README.md](../frontend/README.md). For system-wide design specifications, see the root [README.md](../README.md).

---

## Technical Stack & Microservices

| Service / Component | Technology | Version | Port | Role & Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| **Primary API Server** | FastAPI + Uvicorn | `0.138.1` / `0.49.0` | `8000` | Exposes REST endpoints (`/metrics`, `/metric/{id}`, `/record/{id}`, `/ask`, `/search`, `/health`). |
| **Embedding Microservice**| FastAPI + PyTorch CPU | `0.115.12` | `8001` | Dedicated microservice generating 384-dimensional dense vectors via `all-MiniLM-L6-v2`. |
| **Metrics Warehouse** | Supabase (PostgreSQL 15) | `2.31.0` | `5432` / Cloud | Relational & JSONB metric storage holding all 456 canonical statement records. |
| **Vector Database** | ChromaDB | `1.5.9` | In-process | Persistent vector store caching embeddings for Q1 2026 earnings release notes. |
| **LLM Inference** | Groq Cloud Client | `1.5.0` | Cloud API | Context-grounded financial synthesis. |
| **ETL & Data Loader** | Pandas + Openpyxl | `3.0.3` / `3.1.5` | CLI Tool | Parses canonical mapped KPI metrics with automated backup and upsert verification. |

---

## System Architecture Diagram

```mermaid
graph TD
    %% Clients
    UI["Next.js Client (frontend/)"]

    %% Backend Services Subgraph
    subgraph ComposeStack ["Docker Compose Network (quantumlens-internal)"]
        subgraph APIService ["quantumlens-api (:8000)"]
            Router["FastAPI Web Router (src/api/)"]
            Orchestrator["Agent Orchestrator (src/agents/)"]
            Retriever["Document Retriever (src/rag/)"]
            MetricSvc["Metric Service (src/api/services/)"]
            RecordSvc["Record Service (src/api/services/)"]
        end

        subgraph EmbedService ["embedding-service (:8001)"]
            EmbedApp["Uvicorn ASGI App (app.py)"]
            MiniLM["SentenceTransformers (all-MiniLM-L6-v2)"]
            EmbedHealth["Healthcheck Endpoint (/health)"]
        end

        subgraph StorageLayer ["Persistence Layer"]
            Chroma[("ChromaDB Vector Store<br>[/app/data/vectordb]")]
        end
    end

    %% External Systems
    subgraph ExternalServices ["External Cloud Services"]
        Supabase[("Supabase PostgreSQL<br>[456 Canonical Metrics]")]
        Groq["Groq Cloud API<br>[Llama-3.3 Synthesis]")]
    end

    %% Network Connections
    UI <-->|HTTP REST :8000| Router
    Router --> MetricSvc
    Router --> RecordSvc
    Router --> Orchestrator
    
    MetricSvc <-->|SQL Queries| Supabase
    RecordSvc <-->|SQL Queries| Supabase

    Orchestrator --> Retriever
    Retriever <-->|POST /embed :8001| EmbedApp
    EmbedApp --> MiniLM

    Retriever <-->|Vector Distance Query| Chroma
    Orchestrator <-->|Prompt + Context| Groq

    %% Styling
    classDef client fill:#1f77b4,stroke:#333,stroke-width:2px,color:#fff;
    classDef api fill:#0f172a,stroke:#334155,stroke-width:2px,color:#fff;
    classDef embed fill:#1e293b,stroke:#475569,stroke-width:2px,color:#fff;
    classDef storage fill:#334155,stroke:#64748b,stroke-width:2px,color:#fff;
    classDef cloud fill:#e11d48,stroke:#9f1239,stroke-width:2px,color:#fff;

    class UI client;
    class APIService api;
    class EmbedService embed;
    class StorageLayer storage;
    class ExternalServices cloud;
```

---

## Canonical Data Truth & Verification

The primary source of truth for all financial KPIs is [src/ingestion/mapped_metrics.json](src/ingestion/mapped_metrics.json).

### Metrics Summary Table
| Metric Name | Metric ID | Abbreviation | Sheet Name | Row | Latest Value (P1) | Canonical Rows |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Profit Before Tax (PBT)** | `7` | `pbt` | Group income statement | `13` | `$9,376M` | 90 |
| **Common Equity Tier 1 (CET1)** | `20` | `cet1` | Group balance sheet | `28` | `$129,400M` | 1 |
| **Common Equity Tier 1 Ratio** | `21` | `cet1r` | Capital schedules | `6` | `15.2%` | 1 |
| **Net Interest Income (NII)** | `1` | `nii` | Group income statement | `6` | `$8,945M` | 3 |
| **Net Fee Income** | `2` | `nfi` | Group income statement | `7` | `$3,120M` | 2 |
| **Total Operating Expenses** | `6` | `toe` | Group income statement | `11` | `$8,302M` | 2 |
| **Revenue** | `31` | `rev` | Group income statement | `5` | `$17,042M` | 1 |
| **Customer Accounts** | `18` | `ca` | Group balance sheet | `19` | `$1,612,400M` | 1 |

> [!IMPORTANT]
> The database previously held a stale 366-row dataset missing PBT. Version 10 restores the canonical 456-row dataset with all 90 PBT rows verified in Supabase.

---

## REST Endpoints Reference

| Method | Endpoint | Description | Request Payload | Response Sample |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/health` | API and operational health check. | None | `{"status": "healthy"}` |
| `GET` | `/metrics` | Lists all distinct financial metrics. | None | `[{"metric_id": 7, "metric_name": "profit_before_tax", "abbreviation": "pbt"}]` |
| `GET` | `/metric/{metric_id}` | Returns all sheet rows for a metric. | None | `[{"id": 371, "metric_id": 7, "sheet_name": "Group income statement", "row_number": 13}]` |
| `GET` | `/record/{record_id}` | Retrieves full record with 7 periods. | None | `[{"id": 371, "period_values": [{"period_index": 1, "value": 9376}]}]` |
| `POST`| `/ask` | Semantic RAG pipeline inquiry. | `{"question": "What is PBT?"}` | `{"answer": "Profit Before Tax was $9,376M...", "sources": [...]}` |
| `POST`| `/search` | Direct vector search in ChromaDB. | `{"query": "CET1 ratio", "top_k": 3}` | `[{"text": "At 31 March 2026, CET1 ratio...", "metadata": {...}}]` |
| `POST`| `/agent/query` | Multi-agent orchestrated reasoning. | `{"question": "Show PBT trend"}`| `{"status": "success", "data": {...}}` |

---

## Docker Compose Orchestration

Run services from the `backend/` directory:

```bash
# 1. Build and start both services in detached mode
docker compose up -d --build

# 2. Check service status
docker compose ps

# 3. View logs
docker compose logs -f quantumlens-api
```

### Container Status Verification
| Service | Image | Status | Healthcheck |
| :--- | :--- | :--- | :--- |
| `backend-embedding-service-1` | `backend-embedding-service` | Up (healthy) | Python urllib check against `/health` |
| `backend-quantumlens-api-1` | `backend-quantumlens-api` | Up | Bound to port `0.0.0.0:8000` |

---

## Testing & Quality Assurance

Run the test suite inside the container or locally:

```bash
docker exec backend-quantumlens-api-1 python -m pytest -q
```

### Test Coverage Table
| Test File | Test Case | Target Checked | Result |
| :--- | :--- | :--- | :--- |
| `test_metric_alias_resolution.py` | `test_resolve_known_metric_aliases` | Alias resolution for PBT, CET1, NII | Passed |
| `test_metric_alias_resolution.py` | `test_unknown_metric_is_preserved` | Fallback preservation for unknown terms | Passed |
| `test_metric_alias_resolution.py` | `test_empty_metric_is_empty` | Empty query boundary handling | Passed |
| `test_data_loader.py` | `test_canonical_source_contains_pbt` | Validates 456 total rows and 90 PBT rows | Passed |
| `test_data_loader.py` | `test_payload_maps_canonical_fields` | Payload mapping integrity | Passed |
| `test_document_retriever_validation.py` | `test_document_retriever_empty_question_raises` | Input validation & bounds | Passed |

---

## Environment Variables

| Variable Name | Required | Service | Description | Default |
| :--- | :--- | :--- | :--- | :--- |
| `SUPABASE_URL` | Yes | API | Supabase project URL. | Loaded from `.env` |
| `SUPABASE_KEY` | Yes | API | Supabase Service Role Key for queries. | Loaded from `.env` |
| `GROQ_API_KEY` | Optional | API | Groq API key for Llama-3.3 LLM synthesis. | Loaded from `.env` |
| `EMBEDDING_SERVICE_URL` | Yes | API | URL to embedding microservice. | `http://embedding-service:8001` |
| `VECTOR_DB_PATH` | Yes | API | Local persistent storage for ChromaDB. | `/app/data/vectordb` |

---

## Proprietary License Notice

> **Copyright © 2026 Ved Vivek Talmaley. All Rights Reserved.**  
> *This project and its original source code are strictly proprietary. Unauthorized copying, modification, distribution, or reproduction of this repository, via any medium, is strictly prohibited.*
