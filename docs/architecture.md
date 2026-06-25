# System Architecture

## Ingestion Layer

| Component | Responsibility |
|------------|---------------|
| Workbook Reader | Load Excel workbooks |
| Sheet Scanner | Convert sheets to JSON metadata |

### Flow

Excel Workbook
↓
Workbook Reader
↓
Sheet Scanner
↓
Sheet Metadata

---

## Transformation Layer

| Component | Responsibility |
|------------|---------------|
| Metric Extractor | KPI detection |
| Value Extractor | Numeric extraction |
| Period Mapper | Time-series generation |
| KPI Builder | Business KPI construction |

### Flow

Metadata
↓
Metric Extraction
↓
Value Extraction
↓
Period Mapping
↓
KPI Records

---

## Warehouse Layer

| Component | Responsibility |
|------------|---------------|
| Data Loader | Persist KPI records |
| Query Service | KPI retrieval |

### Flow

KPI Records
↓
Supabase
↓
Query Service

---

## AI Layer

| Component | Status |
|------------|---------|
| Embedding Generator | In Progress |
| Vector Store | Planned |
| Retrieval Engine | Planned |
| RAG Pipeline | Planned |

### Planned Flow

Warehouse
↓
Embeddings
↓
Vector Search
↓
Retriever
↓
LLM

---

## Observability Layer

| Component | Status |
|------------|---------|
| Grafana | Planned |
| Prometheus | Planned |

### Planned Monitoring

- Pipeline Health
- KPI Quality
- Extraction Metrics
- Query Performance
