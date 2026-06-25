# QuantumLens - HSBC Financial Analytics Platform
under construction 
## Project Snapshot

| Attribute                 | Value                                      |
| ------------------------- | ------------------------------------------ |
| Project Name              | QuantumLens                                |
| Domain                    | Financial Analytics                        |
| Data Source               | HSBC Financial Reports                     |
| Input Formats             | Excel, PDF (Planned), PPT (Planned)        |
| Primary Language          | Python                                     |
| Database                  | Supabase (PostgreSQL)                      |
| Current Records Processed | 366 KPI Records                            |
| Current Warehouse Records | 443 Rows                                   |
| Architecture Style        | ETL + Analytics + RAG                      |
| Deployment Goal           | Enterprise Financial Intelligence Platform |

---

## Executive Summary

| Problem                                  | Solution                     |
| ---------------------------------------- | ---------------------------- |
| Financial reports are difficult to query | Automated KPI extraction     |
| KPI names vary across reports            | Metric normalization engine  |
| Manual financial analysis is slow        | Structured warehouse storage |
| Traditional search is limited            | Semantic retrieval           |
| Financial data lacks observability       | Planned monitoring layer     |

---

## End-to-End Pipeline

```text
Excel Reports
      │
      ▼
Workbook Reader
      │
      ▼
Sheet Scanner
      │
      ▼
Metric Extractor
      │
      ▼
Value Extractor
      │
      ▼
Period Mapper
      │
      ▼
KPI Builder
      │
      ▼
Supabase Warehouse
      │
      ▼
Query Service
      │
      ▼
Embedding Generator
      │
      ▼
Vector Search
      │
      ▼
RAG Engine
      │
      ▼
LLM Analytics
```

---

# System Layers

| Layer | Components | Status | Details |
|---------|-----------|---------|---------|
| Ingestion | Workbook Reader, Sheet Scanner | Complete | [View](docs/architecture.md#ingestion-layer) |
| Transformation | Metric Extractor, Value Extractor, Period Mapper, KPI Builder | Complete | [View](docs/architecture.md#transformation-layer) |
| Warehouse | Data Loader, Query Service | Complete | [View](docs/architecture.md#warehouse-layer) |
| AI Layer | Embedding Generator, Retrieval Engine | In Progress | [View](docs/architecture.md#ai-layer) |
| Observability | Grafana, Prometheus | Planned | [View](docs/architecture.md#observability-layer) |

---
## Technology Stack

| Category        | Technologies          |
| --------------- | --------------------- |
| Programming     | Python 3.13           |
| Data Processing | Pandas, NumPy         |
| Storage         | PostgreSQL, Supabase  |
| AI/NLP          | Sentence Transformers |
| Retrieval       | Vector Embeddings     |
| Monitoring      | Prometheus            |
| Visualization   | Grafana               |
| Version Control | Git, GitHub           |

---

## Current Metrics

| Metric                  | Value                |
| ----------------------- | -------------------- |
| Worksheets Scanned      | Multiple HSBC Sheets |
| KPI Catalog Entries     | 53                   |
| KPI Records Generated   | 366                  |
| Database Records Loaded | 443                  |
| Extraction Accuracy     | Under Validation     |
| Duplicate Prevention    | Upsert Enabled       |
| Data Warehouse          | Operational          |

---

## Development Progress

| Module           | Progress |
| ---------------- | -------- |
| Workbook Reader  | 100%     |
| Sheet Scanner    | 100%     |
| Metric Extractor | 100%     |
| Value Extractor  | 100%     |
| KPI Builder      | 100%     |
| Data Loader      | 100%     |
| Query Service    | 100%     |
| Vector Loader    | 0%       |
| Retrieval Engine | 0%       |
| Grafana Layer    | 0%       |
| Prometheus Layer | 0%       |

Overall Backend Completion: ~75%

# Repository Structure

```text
quantumlens-HSBC/
│
├── data/
│   ├── raw/
│   │   └── HSBC Excel Reports
│   │
│   ├── processed/
│   │   ├── scan_sheet_metadata.json
│   │   ├── extracted_metrics.json
│   │   ├── valued_metrics.json
│   │   ├── mapped_metrics.json
│   │   └── kpi_records.json
│
├── src/
│   │
│   ├── ingestion/
│   │   ├── workbook_reader.py
│   │   ├── sheet_scanner.py
│   │   └── metric_extractor.py
│   │
│   ├── transformation/
│   │   ├── value_extractor.py
│   │   ├── period_mapper.py
│   │   └── kpi_builder.py
│   │
│   ├── warehouse/
│   │   ├── supabase_client.py
│   │   ├── data_loader.py
│   │   └── query_service.py
│   │
│   ├── rag/
│   │   ├── embedding_generator.py
│   │   ├── vector_loader.py
│   │   └── retrieval_engine.py
│   │
│   └── config/
│       └── metric_dictionary.json
│
├── docs/
│   ├── architecture.md
│   ├── schemas.md
│   └── troubleshooting.md
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Module Breakdown

| Module                 | Purpose                  | Input           | Output           |
| ---------------------- | ------------------------ | --------------- | ---------------- |
| workbook_reader.py     | Load Excel workbook      | .xlsx           | Workbook Object  |
| sheet_scanner.py       | Scan all sheets and rows | Workbook        | JSON Metadata    |
| metric_extractor.py    | Detect KPI rows          | Sheet Metadata  | KPI Matches      |
| value_extractor.py     | Extract numerical values | KPI Matches     | Numeric Records  |
| period_mapper.py       | Assign reporting periods | Numeric Records | Time-Series Data |
| kpi_builder.py         | Create business KPIs     | Mapped Records  | KPI Objects      |
| data_loader.py         | Load data into warehouse | KPI Objects     | Supabase Records |
| query_service.py       | Retrieve KPI data        | Supabase        | KPI Results      |
| embedding_generator.py | Generate vectors         | KPI Records     | Embeddings       |
| vector_loader.py       | Store embeddings         | Embeddings      | Vector Store     |
| retrieval_engine.py    | Semantic retrieval       | User Query      | Relevant KPIs    |

---

# ETL Pipeline Breakdown

## Stage 1: Workbook Reader

### Responsibility

Load HSBC financial reports into memory.

### Input

```text
260505-1q-2026-data-pack-excel.xlsx
```

### Output

```python
ExcelFile Object
```

### Key Operations

| Operation        | Purpose                       |
| ---------------- | ----------------------------- |
| Workbook Loading | Read Excel file               |
| Sheet Discovery  | Identify worksheet names      |
| Validation       | Ensure workbook accessibility |

---

## Stage 2: Sheet Scanner

### Responsibility

Convert worksheet rows into structured JSON records.

### Output Example

```json
{
  "source_workbook": "260505-1q-2026-data-pack-excel.xlsx",
  "sheet_name": "Credit Risk",
  "row_number": 124,
  "row_values": [
    "At 31 March 2026",
    354763,
    59023
  ],
  "non_null_count": 3
}
```

### Processing Logic

```text
Workbook
    │
    ▼
For Each Sheet
    │
    ▼
For Each Row
    │
    ▼
JSON Record
```

---

## Stage 3: Metric Extractor

### Responsibility

Identify business KPIs using the KPI catalog.

### Example

Input Row:

```text
Net Interest Income | 8945 | 9196
```

Lookup:

```json
{
  "net interest income": {
    "metric_id": 1,
    "abbreviation": "nii"
  }
}
```

Output:

```json
{
  "metric_id": 1,
  "normalized_metric_name": "net_interest_income"
}
```

### Matching Strategy

| Step | Action                |
| ---- | --------------------- |
| 1    | Extract text cells    |
| 2    | Normalize text        |
| 3    | Hash-map lookup       |
| 4    | Retrieve KPI metadata |
| 5    | Create KPI record     |

Complexity:

```text
O(1)
```

per KPI lookup.

---

# KPI Catalog Structure

```json
{
  "net interest income": {
    "metric_id": 1,
    "normalized_metric_name": "net_interest_income",
    "abbreviation": "nii"
  }
}
```

### Benefits

| Benefit         | Description             |
| --------------- | ----------------------- |
| Fast Lookup     | Constant-time access    |
| Consistency     | Standardized names      |
| Scalability     | Easy KPI expansion      |
| Maintainability | Centralized definitions |

---

# Value Extraction Layer

### Responsibility

Extract all numerical values associated with a KPI.

Input:

```json
[
  "Net Interest Income",
  8945,
  9196,
  8777,
  8519
]
```

Output:

```json
{
  "numeric_values": [
    8945,
    9196,
    8777,
    8519
  ]
}
```

### Extraction Logic

```text
Row Values
    │
    ▼
Identify Numeric Cells
    │
    ▼
Collect Values
    │
    ▼
Store Numeric Array
```

---

# Period Mapping Layer

### Responsibility

Convert numeric arrays into time-series structures.

Input:

```json
[
  8945,
  9196,
  8777
]
```

Output:

```json
[
  {
    "period_index": 1,
    "value": 8945
  },
  {
    "period_index": 2,
    "value": 9196
  }
]
```

### Why This Exists

| Problem                  | Solution                |
| ------------------------ | ----------------------- |
| Raw numbers lack context | Attach period metadata  |
| Future trend analysis    | Time-series format      |
| Dashboard compatibility  | Structured observations |

---

# KPI Builder

### Responsibility

Transform extracted metrics into business-ready KPI records.

### Input

```json
{
  "metric_id": 1,
  "period_values": [...]
}
```

### Output

```json
{
  "kpi_id": "KPI_0001",
  "metric_name": "net_interest_income",
  "latest_value": 8945,
  "previous_value": 9196,
  "trend": "down"
}
```

### Trend Engine

| Condition         | Result |
| ----------------- | ------ |
| Latest > Previous | Up     |
| Latest < Previous | Down   |
| Latest = Previous | Flat   |

---

# Current Pipeline Output

| Artifact            | Generated |
| ------------------- | --------- |
| Sheet Metadata      | Yes       |
| Extracted Metrics   | Yes       |
| Numeric Values      | Yes       |
| Time-Series Records | Yes       |
| KPI Records         | Yes       |
| Warehouse Records   | Yes       |

Current KPI Records Generated:

```text
366
```

Current Warehouse Records:

```text
443
```
# Database Schema & Warehouse Design

## Warehouse Architecture

```text
KPI Builder
     │
     ▼
Data Loader
     │
     ▼
Supabase
(PostgreSQL)
     │
     ▼
Query Service
     │
     ▼
Analytics Layer
```

---

## Metrics Table

| Column          | Type      | Description               |
| --------------- | --------- | ------------------------- |
| id              | SERIAL    | Primary Key               |
| metric_id       | INTEGER   | Unique KPI identifier     |
| metric_name     | TEXT      | Normalized KPI name       |
| abbreviation    | TEXT      | Short KPI code            |
| period_values   | JSONB     | Time-series KPI values    |
| source_workbook | TEXT      | Source Excel file         |
| sheet_name      | TEXT      | Source worksheet          |
| row_number      | INTEGER   | Original row location     |
| created_at      | TIMESTAMP | Record creation timestamp |

---

## Example Warehouse Record

```json
{
  "metric_id": 1,
  "metric_name": "net_interest_income",
  "abbreviation": "nii",
  "period_values": [
    {
      "period_index": 1,
      "value": 8945
    },
    {
      "period_index": 2,
      "value": 9196
    }
  ],
  "source_workbook": "260505-1q-2026-data-pack-excel.xlsx",
  "sheet_name": "Group income statement",
  "row_number": 5
}
```

---

## Why JSONB?

| Alternative      | Problem                   |
| ---------------- | ------------------------- |
| Separate Columns | Number of periods changes |
| Separate Tables  | Increased joins           |
| CSV Strings      | Difficult querying        |
| JSONB            | Flexible and queryable    |

---

## KPI Lifecycle

```text
Excel Row
    │
    ▼
Metric Match
    │
    ▼
Numeric Extraction
    │
    ▼
Period Mapping
    │
    ▼
KPI Record
    │
    ▼
Warehouse Record
    │
    ▼
Analytics Query
```

---

# Query Service Design

## Purpose

The Query Service acts as the access layer between applications and the warehouse.

Applications never interact directly with Supabase.

All data access flows through:

```text
Application
      │
      ▼
Query Service
      │
      ▼
Supabase
```

---

## Supported Queries

| Function                   | Purpose                 |
| -------------------------- | ----------------------- |
| get_all_kpis()             | Retrieve all KPIs       |
| get_kpi_by_metric_id()     | Find KPI by ID          |
| get_kpi_by_name()          | Find KPI by name        |
| get_kpis_by_sheet()        | Filter by worksheet     |
| get_kpis_by_abbreviation() | Search by KPI code      |
| get_latest_kpis()          | Retrieve latest records |

---

## Example Query Flow

```text
User Request
      │
      ▼
get_kpi_by_name()
      │
      ▼
Supabase Query
      │
      ▼
JSON Response
```

---

# Engineering Challenges

| Issue | Status | Resolution |
|---------|---------|------------|
| Datetime Serialization | Fixed | ISO conversion |
| NaN JSON Values | Fixed | Converted to None |
| KPI Catalog Coverage | Fixed | Expanded KPI dictionary |
| KPI Matching Logic | Fixed | Hash-map lookup |
| Supabase RLS | Fixed | Service role key |
| Duplicate Records | Fixed | Upsert strategy |
| UTC Deprecation | Fixed | Timezone-aware datetime |
| Row Value Corruption | Fixed | Separate cleaned arrays |

Full details available in [docs/issues.md](docs/issues.md)

# Lessons Learned

| Area            | Key Learning                                                                     |
| --------------- | -------------------------------------------------------------------------------- |
| JSON Processing | Datatypes require normalization                                                  |
| Pandas          | NaN handling is critical                                                         |
| ETL Pipelines   | Data validation must occur early                                                 |
| KPI Extraction  | Domain-specific catalogs improve accuracy                                        |
| Warehousing     | Upserts prevent duplication                                                      |
| Supabase        | RLS policies affect backend access                                               |
| Analytics       | Structured KPIs enable downstream AI workflows                                   |
| Architecture    | Clear separation of ingestion, transformation and storage simplifies maintenance |

---

# Design Principles Followed

| Principle       | Implementation                   |
| --------------- | -------------------------------- |
| Modularity      | Separate pipeline stages         |
| Scalability     | KPI catalog driven extraction    |
| Maintainability | Independent modules              |
| Traceability    | Source workbook tracking         |
| Reusability     | Shared query service             |
| Extensibility   | RAG-ready architecture           |
| Observability   | Future monitoring support        |
| Data Lineage    | Sheet and row tracking preserved |

```
```
