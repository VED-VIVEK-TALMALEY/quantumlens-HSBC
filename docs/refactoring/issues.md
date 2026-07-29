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
