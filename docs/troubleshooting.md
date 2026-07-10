# Troubleshooting Guide and Known Issues

This document details the common troubleshooting steps, pipeline warnings, and historical resolutions for developers working with **QuantumLens**.

For system architecture layouts, see [architecture.md](architecture.md). For table details, see [data_dictionary.md](data_dictionary.md).

---

## Ingestion and Pipeline Issues

### 1. Excel Cell Parse Failures (NaN Issues)
* **Symptom**: Loader scripts crash during transformation, complaining of invalid floats or string elements in numerical arrays.
* **Cause**: Empty or annotated spreadsheet cells parse as `NaN` (Not a Number) in Pandas DataFrames, which are invalid in PostgreSQL JSONB specifications.
* **Resolution**: 
  - Ensure sheet preprocessing handles empty cells using `.replace({np.nan: None})` or similar DataFrame level cleanup.
  - Verify that the [value_extractor.py](../src/transformation/value_extractor.py) isolates true numeric values and discards string notes.

### 2. Missing Period Context in Reports
* **Symptom**: Time-series arrays load into database tables but lack timeline context or appear in the wrong chronological order.
* **Cause**: Column configurations in different workbook files use distinct naming conventions (e.g. "Q1 2026" vs "31 March 2026").
* **Resolution**:
  - Check the relative period indexes mapped by [period_mapper.py](../src/transformation/period_mapper.py).
  - Standardize report timelines to sequential indexes (`period_index: 1`, `period_index: 2`) before SQL load executions.

### 3. Central KPI Catalog Misses
* **Symptom**: The ingestion pipeline skips row items, log files warn of unrecognized metric labels, and records are not loaded into Supabase.
* **Cause**: The worksheet row labels do not match the exact key entries registered in [metric_dictionary.json](../src/config/metric_dictionary.json).
* **Resolution**:
  - Add the unrecognized text label mapping to [metric_dictionary.json](../src/config/metric_dictionary.json) (under lowercase, trimmed constraints).
  - Use exact synonym aliases in the dictionary config to keep matches performing at constant-time speed.

---

## Database Connection and Supabase Issues

### 1. Supabase Row Level Security (RLS) Blocks Ingestion
* **Symptom**: The load process completes without errors but the remote `metrics` table remains empty, or throws a `403 Forbidden` error.
* **Cause**: The database uses Row Level Security policies which block insertion operations unless authenticated.
* **Resolution**:
  - Verify that the loader scripts use the administrative **service role API key** (`SUPABASE_KEY` / `SERVICE_ROLE_KEY`) and not the public key.
  - Check database rules in the Supabase Dashboard to ensure ingestion permissions are correctly assigned.

### 2. Duplicate Record Errors
* **Symptom**: Upload runs crash on unique key violations for `metric_id` or other constraint fields.
* **Cause**: Re-running ingestion files tries to insert rows that already exist in database tables.
* **Resolution**:
  - Use the PostgreSQL `.upsert()` function in the Supabase Python client instead of `.insert()`.
  - Ensure the upsert checks unique constraint identifiers to execute updates instead of inserts.

---

## AI and Vector DB Issues

### 1. Vector DB Path File Errors
* **Symptom**: The retrieval engine complains of missing collection contexts or directory access blockages.
* **Cause**: ChromaDB persistent paths are absolute or reference folders outside the workspace directory structure.
* **Resolution**:
  - Verify that the environment variable `VECTOR_DB_PATH` is configured as a path within the repository root (e.g., `src/rag/vector_db`).
  - Clear the persistent folder database cache and re-run [vector_loader.py](../src/rag/vector_loader.py) to rebuild index spaces.

### 2. High Query Latency on Local Embeddings
* **Symptom**: Calling `/ask` API endpoints takes more than 10 seconds.
* **Cause**: The local SentenceTransformer model (`all-MiniLM-L6-v2`) runs embedding generations on slow CPU hardware instances.
* **Resolution**:
  - Cache database texts and vector lists in [embeddings.json](../src/rag/embeddings.json) during ingestion, so vector indexing runs only once.
  - Ensure the api query pipeline uses direct vector lookups instead of executing database-wide embedding recalculations.

---

## 🔗 Related Documentation
- [Primary Readme](../README.md): Project overview, installation scripts, API reference.
- [System Architecture Spec](architecture.md): Systems layers overview.
- [Database Schema (Data Dictionary)](data_dictionary.md): Detailed columns description.
