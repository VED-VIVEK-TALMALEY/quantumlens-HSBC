<!-- -------------------------------------------------------------------
Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
This project and its source code are strictly proprietary.
Unauthorized copying, distribution, or use is strictly prohibited.
------------------------------------------------------------------- -->

# Database Design & Data Dictionary

This document details the relational data warehouse design, table schemas, indices, and database constraints of **QuantumLens**.

For deployment steps or API integration hooks, see the primary [README.md](../../../README.md). For system architecture diagrams, see [architecture.md](../../architecture/architecture.md).

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
* [Primary Readme](../../../README.md): Project overview, installation scripts, API reference.
* [System Architecture Spec](../../architecture/architecture.md): System layers overview and Mermaid diagrams.
* [KPI Catalog & Normalization Rules](../rag/kpi_catalog.md): Dictionary lookup configurations.
