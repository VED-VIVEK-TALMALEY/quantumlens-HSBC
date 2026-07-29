<!-- -------------------------------------------------------------------
Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
This project and its source code are strictly proprietary.
Unauthorized copying, distribution, or use is strictly prohibited.
------------------------------------------------------------------- -->

# Troubleshooting Guide and Known Issues

This document details the common troubleshooting steps, pipeline warnings, and historical resolutions for developers working with **QuantumLens**.

For system architecture layouts, see [architecture.md](../../docs/architecture/architecture.md). For table details, see [data_dictionary.md](../../docs/features/ingestion/data_dictionary.md).

---

## 1. Ingestion & Pipeline Troubleshooting

| Symptom | Probable Cause | Diagnostic Checklist | Resolution Action |
| :--- | :--- | :--- | :--- |
| **Excel Cell Parse Crash** | Empty, null, or annotated spreadsheet cells parse as `NaN` (Not a Number) in Pandas, which are invalid in PostgreSQL JSONB specifications. | [ ] Check execution logs for `pandas` numeric conversions.<br>[ ] Run the pipeline in dry-run mode and inspect `valued_metrics.json`. | Update sheet preprocessing to handle empty cells using `.replace({np.nan: None})` or similar DataFrame level cleanups in [value_extractor.py](../../backend/src/ingestion/value_extractor.py). |
| **Missing Period Context** | Column timelines in workbook files use distinct naming conventions (e.g. "Q1 2026" vs "31 March 2026"), causing chronological sorting failures. | [ ] Open sheet row headers and confirm column naming formats.<br>[ ] Print output of `period_mapper.py` to confirm the chronological mapping. | Standardize report timelines to sequential indexes (`period_index: 1`, `period_index: 2`) using [period_mapper.py](../../backend/src/transformation/period_mapper.py) before loading. |
| **Central KPI Catalog Skip** | The worksheet row labels do not match the exact key entries registered in [metric_dictionary.json](../../backend/src/ingestion/metric_dictionary.json). | [ ] Look up skipped labels in pipeline execution warnings.<br>[ ] Check if the row label contains leading/trailing whitespaces or numbers. | Add the unrecognized text label mapping to [metric_dictionary.json](../../backend/src/ingestion/metric_dictionary.json) under lowercase, trimmed constraints. |

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
| **High API Query Latency** | SentenceTransformer model (`all-MiniLM-L6-v2`) runs embedding generations on slow CPU hardware instances during boot queries. | [ ] Check API endpoint `/ask` request durations.<br>[ ] Monitor memory (RAM) usage on server boot to identify cold-start bottlenecks. | Cache database texts and vector lists in [embeddings.json](../../backend/data/generated/embeddings.json) during ETL ingestion, loading pre-computed arrays to ChromaDB on startup. |

---

## Related Documentation
* [Primary Readme](../../README.md): Project overview, installation scripts, API reference.
* [System Architecture Spec](../../docs/architecture/architecture.md): Systems layers overview.
* [Database Schema (Data Dictionary)](../../docs/features/ingestion/data_dictionary.md): Detailed columns description.
