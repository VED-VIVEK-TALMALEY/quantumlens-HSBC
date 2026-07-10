# 🗄️ Database Design & Data Dictionary

This document details the relational data warehouse design, table schemas, indices, and database constraints of **QuantumLens**. 

For deployment steps or API integration hooks, see the primary [README.md](../README.md). For systems interaction diagrams, see [architecture.md](architecture.md).

---

## 🏛️ Database Design Rationale

QuantumLens uses **Supabase (PostgreSQL 15)** as its core relational warehouse. The schema is designed around the following engineering choices:
- **Normalized Ingestion Boundaries**: The warehouse maps raw workbook rows to structured records.
- **Dynamic Series (JSONB)**: Financial quarters are not static. Columns representing dates change. Using Postgres JSONB arrays allows storing chronological records of any length within a single row, avoiding frequent schema migrations.
- **Constant-Time Lookups**: Primary keys and unique indices enable quick queries of time-series observations.

---

## 📊 Table Schemas

### 1. `metrics` Table (Operational KPI Warehouse)
The `metrics` table stores normalized KPI records parsed by the ETL loader.

#### Columns Data Dictionary
| Column Name | SQL Type | Nullable | Primary Key | Description / Constraints |
| :--- | :--- | :--- | :--- | :--- |
| **id** | `SERIAL` | NO | YES | Auto-incrementing relational key. |
| **metric_id** | `INTEGER` | NO | NO | Unique metric catalog code mapping (enforces unique constraint). |
| **metric_name** | `TEXT` | NO | NO | Canonical normalized metric name from config dictionary. |
| **abbreviation**| `TEXT` | YES | NO | Associated short name code (e.g. `nii` for net interest income). |
| **period_values**| `JSONB` | NO | NO | Chronological time-series values array of objects. |
| **source_workbook**| `TEXT` | NO | NO | Original Excel file name. |
| **sheet_name** | `TEXT` | NO | NO | Tab worksheet name where the record was found. |
| **row_number** | `INTEGER` | NO | NO | Source spreadsheet row line index (1-indexed). |
| **created_at** | `TIMESTAMP` | NO | NO | Insertion date timestamp (Default `now()`). |

#### `period_values` JSONB Format Schema
The `period_values` column stores a list of chronologically indexed observations. Each object in the array represents a single reporting cycle:
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

---

## ⚡ Query Optimization & Indexes

To keep dashboard queries fast under heavy reading loads, the database is optimized using B-Tree index structures:

| Table Name | Index Name | Columns Indexed | Type | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **metrics** | `metrics_pkey` | `id` | B-Tree | Enforce primary key constraint. |
| **metrics** | `idx_metric_id` | `metric_id` | B-Tree | Optimizes exact matching lookups (e.g., `/metric/{metric_id}`). |
| **metrics** | `idx_metric_name`| `metric_name` | B-Tree | Optimizes query matches (e.g., `get_kpi_by_name()`). |

---

## 🔮 Future Schema Extensions

To transition QuantumLens into a multi-tenant enterprise portal, the database will be extended with the following tables:

### 1. `users` Table
Stores registered platform analysts.
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'analyst' CHECK (role IN ('analyst', 'manager', 'administrator')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

### 2. `dashboards` Table
Maintains user-customized analytical widgets configurations.
```sql
CREATE TABLE dashboards (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    config JSONB DEFAULT '{}'::jsonb NOT NULL,
    is_public BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

### 3. `reports` Table
Stores static regulatory drafts and KPI cohort compilations.
```sql
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    dashboard_id INTEGER NOT NULL REFERENCES dashboards(id) ON DELETE CASCADE,
    summary TEXT,
    metric_snapshots JSONB NOT NULL,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

### 4. `chat_history` Table
Caches conversation contexts for semantic search context checks.
```sql
CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(100) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    sources JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_chat_session ON chat_history(session_id);
```

---

## 🔗 Related Documentation
- [Primary Readme](../README.md): Project overview, installation scripts, API reference.
- [System Architecture Spec](architecture.md): Systems layers overview and Mermaid diagrams.
- [KPI Catalog & Normalization Rules](kpi_catalog.md): Dictionary lookup catalog.
