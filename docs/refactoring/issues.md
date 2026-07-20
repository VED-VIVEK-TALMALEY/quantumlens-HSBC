# Engineering History: Issues, Investigations, and Resolutions

This document records the comprehensive engineering history of QuantumLens. It documents the critical issues encountered during development, the root causes identified, the investigation workflows, the specific code corrections, and the long-term architectural prevention strategies.

---

## 1. JSON Serialization Failure

| Parameter | Details |
| :--- | :--- |
| **Severity** | High |
| **Category** | API / Serialization |
| **Date** | 2026-01-10 |

### Symptoms
The application threw the following stack trace during ETL transformation operations and API response serialization:
```text
TypeError: Object of type Timestamp is not JSON serializable
```
All API calls returning metric lists crashed with HTTP 500 Internal Server Errors.

### Root Cause
When the ingestion layer reads raw Excel sheets via Pandas, date fields are parsed into native `pandas.Timestamp` structures. The standard Python `json` library and default FastAPI JSON response encoders do not have built-in serialization schemas for Pandas `Timestamp` or standard Python `datetime` objects, causing serialization to crash.

### Investigation Process
1. Checked the stack trace to trace where the serialization failure occurred.
2. Verified that it failed inside the API router serialization pipeline when converting model records.
3. Inspected the output of [kpi_builder.py](../src/transformation/kpi_builder.py) and confirmed that raw datetime entries were being passed to database load payloads.

### Solution
Normalized all temporal properties to standard string formats at the transformation layer boundary before database insertion or API response rendering. Specifically, converted timestamps using the ISO-8601 standard `.isoformat()` method.

### Code Changes
```python
# Modified src/transformation/kpi_builder.py
def format_timestamp(ts):
    if hasattr(ts, "isoformat"):
        return ts.isoformat()
    return str(ts)
```

### Lessons Learned
* Standardize temporal properties at the ingestion entry point.
* Always enforce string boundaries for data formats (like ISO-8601) when crossing boundary lines between backend and databases.

### Future Prevention
Integrated strict Pydantic models with automated serializers that raise validation warnings during test executions if non-serializable objects are passed.

---

## 2. NaN Values Breaking JSON

| Parameter | Details |
| :--- | :--- |
| **Severity** | High |
| **Category** | Ingestion / Data Pipeline |
| **Date** | 2026-01-12 |

### Symptoms
FastAPI endpoint validations failed, and Supabase client insertions raised SQL parsing exceptions due to invalid JSON tokens (`NaN` instead of `null`).

### Root Cause
Pandas represents empty or blank cells as `numpy.nan` (floating point Not-a-Number). The standard Python `json` encoder serializes these values as the token `NaN` in raw strings. However, the JSON standard does not recognize `NaN` as a valid token (only `null` is supported), causing relational databases and API clients to reject the payload.

### Investigation Process
1. Inspected intermediate outputs in `data/processed/mapped_metrics.json`.
2. Found raw `NaN` values nested within database arrays.
3. Printed cell datatypes inside [value_extractor.py](../src/transformation/value_extractor.py), which confirmed they were parsed as floating-point NaNs.

### Solution
Normalized all `nan` parameters to standard Python `None` objects before serialization. This ensures that the JSON compiler writes them as valid `null` tokens.

### Data Types Comparison Table
| Type | Python Representation | JSON Serialization | SQL Translation | Behavioral Classification |
| :--- | :--- | :--- | :--- | :--- |
| **NaN** | `float('nan')` / `np.nan` | `NaN` (Invalid JSON) | `NaN` (Float only) | Numeric error state (Not-a-Number) |
| **None** | `None` | `null` | `NULL` | Void/absence of a value |
| **NULL** | `None` | `null` | `NULL` | Unallocated database cell |

### Code Changes
```python
# Modified src/transformation/value_extractor.py
import pandas as pd
import numpy as np

def clean_value(val):
    if pd.isna(val) or val is np.nan:
        return None
    return float(val)
```

### Lessons Learned
* Clean dataframe values before converting them to dictionary payloads.
* Standardize on standard Python types (`None`, `dict`, `list`) for pipeline boundaries.

### Future Prevention
Added a global validator hook in Pydantic settings that filters and replaces floating-point NaNs with `None` during deserialization.

---

## 3. Metric Normalization Problems

| Parameter | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Category** | Data Transformation |
| **Date** | 2026-01-15 |

### Symptoms
The database ended up with multiple separate records representing the same metric under different names (e.g. "Total Revenue", "Operating Revenue", "Revenue"). This prevented time-series tracking and cohort analysis.

### Root Cause
Financial statements use inconsistent naming conventions. Row names and labels vary between quarters and sheet formats. Without a normalization engine, the system treats each variation as a distinct database metric.

### Investigation Process
1. Audited the `metrics` table in Supabase.
2. Found multiple instances of the same business metric stored under separate IDs.
3. Checked [metric_extractor.py](../src/ingestion/metric_extractor.py) and found it was performing loose substring lookups without a mapped catalog.

### Solution
Created a centralized catalog mapping ([metric_dictionary.json](../src/config/metric_dictionary.json)) that acts as a lookup hash map. This maps raw row names to standard metric IDs and abbreviation codes.

### Normalization Mapping Table
| Input String Variant | Normalized Token | Assigned Metric ID | Abbreviation | Business Context |
| :--- | :--- | :--- | :--- | :--- |
| "Total Revenue" | `revenue` | 3 | `rev` | Top-line sales |
| "Operating Revenue" | `revenue` | 3 | `rev` | Top-line sales |
| "Net Revenue" | `revenue` | 3 | `rev` | Top-line sales |
| "Net Interest Income"| `net_interest_income`| 1 | `nii` | Banking net yield |

### Code Changes
```python
# Modified src/ingestion/metric_extractor.py
import json

def normalize_name(raw_name):
    clean_token = " ".join(raw_name.lower().split())
    # Query dictionary catalog
    match = metric_dictionary.get(clean_token)
    if match:
         return match["metric_id"], match["normalized_metric_name"]
    return None, None
```

### Lessons Learned
* Never use loose substring lookups for business-critical entity classification.
* Standardize on a centralized catalog config file to manage naming synonyms.

### Future Prevention
Added a validation script that alerts developers during the build stage if a scanned workbook row name is skipped by the normalization dictionary.

---

## 4. Duplicate Database Records

| Parameter | Details |
| :--- | :--- |
| **Severity** | High |
| **Category** | Database Storage |
| **Date** | 2026-01-18 |

### Symptoms
Re-running the ETL pipelines multiplied the table row counts in the database, generating duplicate data points for identical periods and workbook targets.

### Root Cause
The database loader script used standard PostgreSQL `INSERT` queries without unique key checks. Since the database schema did not enforce constraints on the `metric_id` field, database records duplicated on every script execution.

### Investigation Process
1. Checked row counts in the Supabase dashboard.
2. Ran a SQL query checking the occurrence of identical metric names:
   ```sql
   SELECT metric_id, COUNT(*) FROM metrics GROUP BY metric_id HAVING COUNT(*) > 1;
   ```
3. Confirmed that duplicates existed across similar source workbooks.

### Solution
Enforced a `UNIQUE` constraint on the `metric_id` column in the PostgreSQL schema. Replaced insert calls with `.upsert()` queries in [data_loader.py](../src/warehouse/data_loader.py) to overwrite existing records on key conflicts.

### Database Operations Table
| Command Pattern | Action on Constraint Conflict | Table Growth Profile | Duplicate Hazard |
| :--- | :--- | :--- | :--- |
| **Insert** | Throws error (with unique key constraint) / appends rows (without constraint). | Exponential | High |
| **Upsert (Current)**| Overwrites existing record columns. | Linear (One row per ID) | None |

### Code Changes
```sql
-- Migration: Add unique constraint
ALTER TABLE metrics ADD CONSTRAINT unique_metric_id UNIQUE (metric_id);
```
```python
# Modified src/warehouse/data_loader.py
def load_records(payload):
    # Execute upsert check on unique constraint
    result = supabase.table("metrics").upsert(payload).execute()
    return result
```

### Lessons Learned
* Relational tables storing state configurations must enforce unique constraints.
* Prefer upsert operations for data loading tasks to prevent data duplication.

### Future Prevention
Integrated integration tests that run the ETL pipeline twice and verify that the database table row count remains identical.

---

## 5. Supabase Authentication Issues

| Parameter | Details |
| :--- | :--- |
| **Severity** | Critical |
| **Category** | Security / Database Connection |
| **Date** | 2026-01-20 |

### Symptoms
Write operations from ETL loader scripts failed with `401 Unauthorized` or `403 Forbidden` database errors, while local API reads worked correctly.

### Root Cause
The write connections used the default public `anon` API key. Since Row Level Security (RLS) policies were active on the database, anonymous insertions were blocked. Write operations require administrative privileges, which are managed by the database service key.

### Investigation Process
1. Checked connection variables in [supabase_client.py](../src/warehouse/supabase_client.py).
2. Verified that the API requests were using the `anon` key from env configurations.
3. Inspected RLS logs in the Supabase dashboard console, confirming blocked insertion actions.

### Solution
Updated the ETL ingestion scripts to connect using the administrative service key (`SUPABASE_KEY` / `SERVICE_ROLE_KEY`), while keeping the public `anon` key restricted to read-only API calls.

### API Credentials Access Matrix
| Key Variant | Security Isolation | Allowed Operations | Safe for Frontend? | Bypass RLS? |
| :--- | :--- | :--- | :--- | :--- |
| **Anon Key** | Enforced by policies | SELECT | Yes | No |
| **Service Key**| Enforced at engine level | SELECT, INSERT, UPDATE, DELETE | No (Keep secret) | Yes |

### Code Changes
```python
# Modified src/warehouse/supabase_client.py
import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
# Initialize using administrative service key
SUPABASE_KEY = os.getenv("SUPABASE_KEY") 

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

### Lessons Learned
* Explicitly separate database connection roles for client applications and ETL operations.
* Never expose the service role key in client-side code or public repositories.

### Future Prevention
Configured CI/CD scanning rules that detect and block commits containing hardcoded service role credentials.

---

## 6. Datetime UTC Deprecation

| Parameter | Details |
| :--- | :--- |
| **Severity** | Low |
| **Category** | Python Runtime |
| **Date** | 2026-01-22 |

### Symptoms
The application console logged the following deprecation warning on Python 3.13 startup:
```text
DeprecationWarning: datetime.datetime.utcfromtimestamp() is deprecated and scheduled for removal in Python 3.13
```

### Root Cause
Python 3.13 deprecates naive UTC datetime creation methods because they do not include timezone offset information, which can lead to localized time conversion errors. Modern runtimes require timezone-aware datetime objects.

### Investigation Process
1. Traced runtime warning prints to timestamp logs.
2. Found instances of `datetime.utcnow()` and `datetime.utcfromtimestamp()` in data format helpers.

### Solution
Updated all datetime creation logic to use timezone-aware objects with explicit UTC offsets: `datetime.now(datetime.timezone.utc)`.

### Code Changes
```python
# Modified src/api/services.py
from datetime import datetime, timezone

def generate_record_timestamp():
    # Replace datetime.utcnow()
    return datetime.now(timezone.utc).isoformat()
```

### Lessons Learned
* Avoid timezone-naive datetime objects.
* Explicitly define the timezone offset (UTC) for datetime values.

### Future Prevention
Configured testing tools to treat Python deprecation warnings as errors, blocking builds containing deprecated datetime calls.

---

## 7. KPI Extraction Errors

| Parameter | Details |
| :--- | :--- |
| **Severity** | High |
| **Category** | Ingestion / Parser |
| **Date** | 2026-01-25 |

### Symptoms
The system logged false positives (e.g. matching "Tax on Net Fee Income" as "Net Fee Income") and false negatives (missing actual KPIs due to slight variation differences).

### Root Cause
The matching engine relied on simple substring lookups. Without strict boundary checks, this led to incorrect matches on nested labels.

### Investigation Process
1. Inspected [metric_extractor.py](../src/ingestion/metric_extractor.py) row parsing loops.
2. Verified that string checks like `if "fee income" in row_text` matched unintended rows (e.g., "Tax on Net Fee Income").
3. Logged matching accuracy targets in test sheets.

### Solution
Replaced loose substring lookups with strict matches on lowercase, stripped string tokens. Implemented exact regex checks to prevent matching nested substrings.

### Extraction Accuracy Table
| String Input | Substring Result | Clean Regex Result | Status Classification |
| :--- | :--- | :--- | :--- |
| "Net Fee Income" | Match | Match | Correct Match |
| "Tax on Net Fee Income"| Match | No Match | Avoided False Positive |
| "Fee Income Note" | Match | No Match | Avoided False Positive |

### Code Changes
```python
# Modified src/ingestion/metric_extractor.py
import re

def clean_row_label(label):
    # Remove excess padding and leading strings
    clean = label.strip().lower()
    clean = re.sub(r'^(total|net|gross)\s+', '', clean)
    return clean
```

### Lessons Learned
* Do not rely on loose substring checks for entity matching.
* Use exact regular expression rules or hash lookup maps to ensure matching accuracy.

### Future Prevention
Added a test dataset of common financial labels to evaluate extractor matching accuracy during builds.

---

## 8. Period Mapping Challenges

| Parameter | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Category** | Transformation |
| **Date** | 2026-01-28 |

### Symptoms
Time-series graphs displayed values out of order, and the AI model failed to accurately interpret trend directions because raw metrics lacked explicit date bounds.

### Root Cause
Spreadsheet cells contain numerical arrays without explicit period keys (e.g. `[8945, 9196, 8777]`). The timeline context is often defined separately in top-row header cells, making it difficult to align raw row values.

### Investigation Process
1. Inspected parsed payloads in `data/processed/valued_metrics.json`.
2. Verified that data points were stored as plain arrays without index mappings.
3. Confirmed that different sheets ordered data columns differently (e.g., chronological vs reverse-chronological).

### Solution
Created a period mapping engine in [period_mapper.py](../src/transformation/period_mapper.py). This maps raw numeric columns to sequential reporting periods (`period_index`), and sorts arrays chronologically to standardize trend calculations.

### Ingestion Period Mapping Schema
```text
Raw Excel Layout:  [Column B: 4Q25] [Column C: 1Q26] [Column D: 2Q26]
                          │               │               │
                          ▼               ▼               ▼
Database JSONB:     [Period ID: 1]  [Period ID: 2]  [Period ID: 3]
```

### Code Changes
```python
# Modified src/transformation/period_mapper.py
def map_periods(numeric_list, chronological=True):
    mapped = []
    # Enforce order directions
    iterator = enumerate(numeric_list) if chronological else enumerate(reversed(numeric_list))
    for idx, val in iterator:
        mapped.append({
            "period_index": idx + 1,
            "value": val
        })
    return mapped
```

### Lessons Learned
* Convert positional arrays to explicit key-value structures before database storage.
* Always enforce chronological sorting for time-series records to simplify downstream trend analysis.

### Future Prevention
Extended the JSONB schema configuration to support explicit string date labels (e.g., `"2026-Q1"`) alongside sequential period IDs.

---

## 9. Excel Ingestion Parsing Issues

| Parameter | Details |
| :--- | :--- |
| **Severity** | High |
| **Category** | Ingestion |
| **Date** | 2026-02-02 |

### Symptoms
The ingestion pipeline failed to process spreadsheets containing merged title blocks, empty rows, hidden reference sheets, or formula expressions instead of raw values.

### Root Cause
Financial workbooks use complex layouts for human readability (merged headers, blank spacing columns, and live Excel formulas). Standard `pd.read_excel()` calls import these as empty/NaN fields or parse formulas as string equations, breaking downstream loaders.

### Investigation Process
1. Inspected parser executions using debugger break points.
2. Verified that merged header columns returned empty values for all but the first cell.
3. Found that formula cells imported the underlying equation string (e.g. `"=SUM(B12:B14)"`) instead of the evaluated number.

### Solution
1. Configured the pandas engine to load calculated cell values instead of raw formula strings (`data_only=True` via `openpyxl`).
2. Implemented programmatic forward-fill checks to resolve merged cells.
3. Ignored blank rows and hidden sheets by validating columns before processing.

### Excel Layout Parsing Matrix
| Cell State | Raw Pandas Result | Clean Ingestion Result | Process Action |
| :--- | :--- | :--- | :--- |
| **Merged Title** | `["Revenue", NaN, NaN]` | `["Revenue", "Revenue", "Revenue"]` | Forward-fill cells |
| **Formula Cell** | `"=SUM(B5:B7)"` | `12450.0` | Read calculated values |
| **Empty Spacing Row**| `[NaN, NaN, NaN]` | Skip Row | Filter null rows |

### Code Changes
```python
# Modified src/ingestion/sheet_scanner.py
def parse_secure_workbook(file_path):
    # Force calculated values resolution
    import openpyxl
    wb = openpyxl.load_workbook(file_path, data_only=True)
    return wb
```

### Lessons Learned
* Parse evaluated cell values instead of formula strings.
* Standardize on clear pre-filtering rules to clean up merged header layout cells.

### Future Prevention
Implemented a validation step that raises alerts if the parser encounters raw formula strings during ingestion.

---

## 10. ChromaDB Integration

| Parameter | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Category** | AI Layer |
| **Date** | 2026-02-05 |

### Symptoms
The semantic search engine returned empty query results or failed with folder access blockages on startup, and embedding calculations delayed system boot times.

### Root Cause
ChromaDB persistent database paths were misconfigured, and the system regenerated all vector embeddings on every startup instead of loading cached indices.

### Investigation Process
1. Inspected log files in `logs/quantumlens.log`.
2. Verified that vector store folders were created outside the target workspace directory.
3. Measured model execution times, which confirmed a cold-start delay of over 45 seconds due to embedding regeneration.

### Solution
1. Configured ChromaDB to use a persistent local directory in [settings.py](../src/config/settings.py).
2. Saved generated embeddings to [embeddings.json](../src/rag/embeddings.json) during ingestion.
3. Updated the startup routine to load cached embeddings directly to ChromaDB on boot, eliminating runtime generation latency.

### Database Connection Schema
```text
ETL Loader ──► [Embeddings JSON Cache] ──► [Local ChromaDB Client] ──► Query Engine
                                                   ▲
                                                   │ Persistence Target
                                          [src/rag/vector_db]
```

### Code Changes
```python
# Modified src/rag/vector_loader.py
import chromadb
from src.config.settings import settings

def load_vectors():
    # Enforce persistent local client connections
    client = chromadb.PersistentClient(path=str(settings.VECTOR_DB_PATH))
    collection = client.get_or_create_collection("hsbc_kpis")
    # Read pre-computed embeddings
    records = read_cached_embeddings()
    collection.add(
        ids=records["ids"],
        embeddings=records["vectors"],
        documents=records["texts"],
        metadatas=records["metadatas"]
    )
```

### Lessons Learned
* Cache vector embeddings to avoid expensive runtime regenerations.
* Configure persistent directory paths within the project workspace to ensure portability.

### Future Prevention
Added a health check that verifies vector database counts on system boot before exposing API routes.

---

## 11. RAG Quality Problems

| Parameter | Details |
| :--- | :--- |
| **Severity** | High |
| **Category** | AI Layer |
| **Date** | 2026-02-08 |

### Symptoms
The RAG pipeline returned incorrect numbers, referenced metrics from unrelated spreadsheet sheets, or exceeded the maximum token window limits of the LLM.

### Root Cause
The semantic search query returned raw documents that contained formatting notes instead of clean database context, or the top-K query parameter pulled unrelated rows, diluting the context window.

### Investigation Process
1. Captured prompt context payloads sent to the Groq API.
2. Checked prompt structures, showing unformatted text chunks that confused the LLM.
3. Found that cosine similarity scores were too low, indicating weak match filtering.

### Solution
1. Refactored the document generation model to pre-structure records as clean key-value pairs (metric, workbook, sheet, row, period values).
2. Implemented cosine distance thresholds to exclude weak vector matches.

### Prompt Context Quality Matrix
| Ingest Context | Formatting Profile | Resulting Accuracy | Token Footprint |
| :--- | :--- | :--- | :--- |
| **Raw Text Chunks** | Ingestion dump strings | Low (Hallucination risk) | High |
| **Structured JSON** | Explicit keys and arrays | High (Accurate counts) | Low |

### Code Changes
```python
# Modified src/rag/prompt_builder.py
def build_prompt(question, retrieved_docs):
    context = ""
    for doc in retrieved_docs:
        # Format as clean key-value segments
        context += f"Metric: {doc['metric_name']}\nValues: {doc['values']}\nSource: {doc['sheet']}\n\n"
        
    return f"Use ONLY the following context to answer:\n{context}\nQuestion: {question}"
```

### Lessons Learned
* Raw string database dumps make poor RAG context. Format retrieved context as clean key-value pairs.
* Apply strict distance thresholds to vector query matches to filter out irrelevant records.

### Future Prevention
Integrated evaluation scripts that measure retrieval precision and response accuracy against a curated set of financial questions.

---

## 12. CORS Deployment Failure

| Parameter | Details |
| :--- | :--- |
| **Severity** | Critical |
| **Category** | Cloud Deployment |
| **Date** | 2026-02-12 |

### Symptoms
The frontend dashboard loaded but failed to retrieve API data. The browser console logged the following error:
```text
Access to XMLHttpRequest at 'https://quantumlens-api.render.com/metrics' from origin 'https://quantumlens-hsbc.vercel.app' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

### Root Cause
FastAPI CORS middleware was configured to only allow requests from `localhost`. When the frontend was deployed to Vercel, requests from the production URL were blocked by the browser.

### Investigation Process
1. Inspected browser developer tools network logs.
2. Verified that API request headers were sent but blocked on preflight checks.
3. Checked CORS middleware settings in [main.py](../src/api/main.py).

### Solution
Updated the FastAPI CORS middleware initialization in [main.py](../src/api/main.py) to whitelist the production frontend domain deployed on Vercel.

### Code Changes
```python
# Modified src/api/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://quantumlens-hsbc.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Lessons Learned
* Explicitly configure allowed origin domains for all target environments (local, staging, production).
* Ensure preflight options are whitelisted for production APIs.

### Future Prevention
Added an environment validation script that dynamically checks and updates whitelisted CORS domains during the deployment stage.

---

## 13. Environment Variable Failures

| Parameter | Details |
| :--- | :--- |
| **Severity** | High |
| **Category** | Configuration |
| **Date** | 2026-02-15 |

### Symptoms
The API server failed to boot on startup or crashed during database queries, raising `KeyError` warnings for missing variables (e.g. `SUPABASE_URL`).

### Root Cause
Environment variables were not initialized in the local shell environment or target deployment dashboards on Render and Vercel.

### Investigation Process
1. Checked system logs in the Render console.
2. Verified that `os.getenv` calls returned `None` for database credentials.
3. Inspected configuration settings in [settings.py](../src/config/settings.py).

### Solution
1. Integrated `python-dotenv` in settings loaders to read `.env` configuration files for local development.
2. Added default fallback settings to prevent startup crashes.
3. Configured required environment variables in the Render and Vercel deployment dashboards.

### Environment Configuration Matrix
| Environment | Key Location | Config Target | Load Tool |
| :--- | :--- | :--- | :--- |
| **Local Development** | `.env` File | Localhost endpoints | `python-dotenv` |
| **Backend Deployed** | Render dashboard | Supabase DB, Groq keys | Native Env Injection |
| **Frontend Deployed** | Vercel dashboard | Deployed backend URL | Native Env Injection |

### Code Changes
```python
# Modified src/config/settings.py
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    # Fallback to local paths
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "src/rag/vector_db")
```

### Lessons Learned
* Always define fallback values for non-critical configuration variables.
* Enforce variable checks on startup to fail fast if critical credentials are missing.

### Future Prevention
Added startup validation checks that verify all required environment variables are populated on boot.

---

## 14. Vercel Framework Detection

| Parameter | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Category** | Deployment |
| **Date** | 2026-02-18 |

### Symptoms
Vercel build executions failed, trying to compile the Python backend or ignoring the frontend `package.json` configurations.

### Root Cause
The repository is structured as a monorepo containing both the FastAPI backend and Next.js frontend projects. Vercel detected the repository root on import and failed to locate the frontend subfolder settings.

### Investigation Process
1. Checked build logs in the Vercel deployment console.
2. Verified that the builder was searching for package configurations in the root directory rather than in `quantumlens-dashboard/`.

### Solution
Updated the Vercel project configurations to set `quantumlens-dashboard` as the root directory, pointing build commands to the correct subfolder package settings.

### Project Build Paths Schema
```text
Root folder (quantumlens-HSBC)
 ├── src/ (Python Backend)
 └── quantumlens-dashboard/  ◄── Configure as Vercel build target root
      ├── package.json
      └── app/ (Next.js Application)
```

### Lessons Learned
* Clearly configure build folder targets when deploying monorepo structures.
* Ensure frontend and backend configurations remain isolated.

### Future Prevention
Added a `vercel.json` configuration file at the repository root to explicitly define routing and build parameters.

---

## 15. Render Deployment Issues

| Parameter | Details |
| :--- | :--- |
| **Severity** | High |
| **Category** | Cloud Deployment |
| **Date** | 2026-02-20 |

### Symptoms
The backend service failed to build on Render, throwing `ModuleNotFoundError` warnings or running out of memory during startup.

### Root Cause
The python package manager failed because dependencies (such as `uvicorn` and `gunicorn`) were missing from `requirements.txt`. Additionally, loading the SentenceTransformer model on small Render instances exceeded memory limits (RAM).

### Investigation Process
1. Inspected build logs in the Render console.
2. Found that the server crashed with Out of Memory (OOM) errors during model initialization.
3. Verified that the start command pointed to incorrect module paths.

### Solution
1. Added missing production dependencies (`uvicorn`, `gunicorn`) to `requirements.txt`.
2. Updated startup module paths.
3. Used a lightweight embedding model (`all-MiniLM-L6-v2`) to reduce memory consumption on low-RAM hosts.

### Host Performance Requirements Table
| Resource Target | Allocation profile | Embedding Latency | RAM Consumption | OOM Risk |
| :--- | :--- | :--- | :--- | :--- |
| **High GPU Host** | > 16GB VRAM | < 5ms | > 4GB | Very Low |
| **Low RAM Host (Render)**| < 512MB RAM | 150-300ms | < 200MB | Low (with MiniLM) |

### Code Changes
```text
# Added to requirements.txt
uvicorn==0.49.0
gunicorn==21.2.0
sentence-transformers==5.6.0
```

### Lessons Learned
* Add production hosting packages (such as `gunicorn`) to dependency files.
* Test model memory usage on lower-tier host specs before production deployment.

### Future Prevention
Configured resource limits on local development servers to simulate production hosting environments.

---

## 16. Localhost vs Production API

| Parameter | Details |
| :--- | :--- |
| **Severity** | High |
| **Category** | Integration |
| **Date** | 2026-02-22 |

### Symptoms
The deployed dashboard frontend loaded correctly but failed to fetch data, attempting to send requests to `http://127.0.0.1:8000` instead of the production API.

### Root Cause
The API URL was hardcoded to `127.0.0.1:8000` in the frontend Axios client settings, which worked locally but failed in production.

### Investigation Process
1. Opened the browser console and checked network requests.
2. Confirmed that API calls were routed to the local host address.
3. Found hardcoded URL parameters in the frontend API client.

### Solution
Refactored the API connection layer to use environment variables (`NEXT_PUBLIC_API_URL`) to dynamically route requests based on the host environment.

### API Routing Configurations Table
| Environment | Key Value | Host Target | Target Endpoint |
| :--- | :--- | :--- | :--- |
| **Local Development** | `http://localhost:8000` | Localhost | Local FastAPI server |
| **Production Build** | `https://quantumlens-api.render.com`| Render Host | Live production API |

### Code Changes
```typescript
// Modified quantumlens-dashboard/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
});

export default api;
```

### Lessons Learned
* Never hardcode API host addresses in frontend client configurations.
* Use environment variables to manage configuration parameters across development environments.

### Future Prevention
Added a build check that fails compile operations if hardcoded localhost URLs are detected in source code files.

---

## 17. Chart Rendering Problems

| Parameter | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Category** | Frontend UI |
| **Date** | 2026-02-25 |

### Symptoms
The dashboard charts rendered empty lines, displayed quarters out of order (e.g. Q4 showing before Q2), or crashed when loading large datasets.

### Root Cause
The graphing library expected sorted data coordinates (e.g., `[{x: period, y: value}]`). The API returned unsorted JSON arrays containing metadata, which confused the frontend graph mapping logic.

### Investigation Process
1. Logged API JSON payloads received by dashboard components.
2. Verified that time-series arrays were unsorted.
3. Found that string dates (e.g. "31 March 2026") were passed directly as coordinate indices, which the graphing library failed to parse.

### Solution
Parsed and sorted `period_values` chronologically by sequence index on the client side before passing the data to the graphing library.

### Chart Coordinate Formatting Schema
```text
Unordered API Payload:   [{period: 2, val: 9196}, {period: 1, val: 8945}]
                                       │
                                       ▼ (Sort by index)
Clean Chart Datasets:    [{period: 1, val: 8945}, {period: 2, val: 9196}]
```

### Code Changes
```typescript
// Modified quantumlens-dashboard/components/TimeSeriesChart.tsx
const prepareChartData = (periodValues: any[]) => {
  return periodValues
    .map(item => ({
      name: `Period ${item.period_index}`,
      value: item.value
    }))
    .sort((a, b) => a.name.localeCompare(b.name));
};
```

### Lessons Learned
* Standardize data shapes on the API level before sending them to the client.
* Sort datasets on the client side to prevent chart rendering errors.

### Future Prevention
Added unit tests for frontend graphing components to verify rendering stability against unsorted datasets.

---

## 18. Frontend State Management

| Parameter | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Category** | Frontend UI |
| **Date** | 2026-02-28 |

### Symptoms
The analytics dashboard experienced performance lag, and selected filter states reset unexpectedly after search updates or panel transitions.

### Root Cause
The dashboard used a single, large state object. Updating any individual filter forced a full re-render of all charts and tables, causing performance lag.

### Investigation Process
1. Analyzed dashboard component execution loops using React Developer Tools.
2. Identified redundant re-renders in charting modules.
3. Found that parent state hooks updated downstream parameters unnecessarily.

### Solution
Decoupled state management by splitting the monolithic state object into focused hooks (`selectedMetric`, `selectedRecord`, `searchQuery`), reducing redundant re-renders.

### State Optimization Table
| Strategy | Rendering Performance | Component Isolation | Complexity |
| :--- | :--- | :--- | :--- |
| **Monolithic State** | Low (Full page re-renders) | Weak (Interdependent modules) | Simple |
| **Decoupled Hooks (Current)**| High (Targeted re-renders) | Strong (Independent components) | Medium |

### Code Changes
```typescript
// Modified quantumlens-dashboard/app/dashboard/page.tsx
const [selectedMetric, setSelectedMetric] = useState<number | null>(null);
const [selectedRecord, setSelectedRecord] = useState<any | null>(null);
const [searchQuery, setSearchQuery] = useState<string>("");
```

### Lessons Learned
* Keep state close to the components that use it to avoid redundant rendering.
* Decouple unrelated state variables in complex UI dashboards to improve page performance.

### Future Prevention
Implemented React rendering profiling checks in the development pipeline to monitor component update cycles.

---

## 19. AI Assistant Development

| Parameter | Details |
| :--- | :--- |
| **Severity** | Medium |
| **Category** | AI Layer |
| **Date** | 2026-03-05 |

### Symptoms
The AI assistant generated overly verbose answers, struggled with fuzzy financial queries, and failed to reference data sources (workbook, sheet, and row).

### Root Cause
The system prompt lacked explicit rules. Without structured instructions, the LLM defaulted to conversational answers, ignoring source citation constraints.

### Investigation Process
1. Analyzed query response logs in [rag_pipeline.py](../src/rag/rag_pipeline.py).
2. Found that the LLM was using general knowledge instead of restricting its context to the retrieved records.

### Solution
Refactored system prompts to define the LLM's role as a financial copilot. Added constraints requiring the model to cite exact source worksheets and filenames, and to output answers in markdown bullet points.

### Code Changes
```python
# Modified src/rag/prompt_builder.py
def build_prompt(question, retrieved_docs):
    context = ""
    for doc in retrieved_docs:
         context += f"Source File: {doc.get('source_workbook')}\nSheet: {doc.get('sheet_name')}\nValues: {doc.get('period_values')}\n\n"
         
    return f"""You are a financial analyst copilot.
    
Rules:
1. Restrict your answer strictly to the context below.
2. Quote exact numbers and sources.
3. If context is insufficient, state that the data is not available.

Context:
{context}

Question: {question}"""
```

### Lessons Learned
* Configure RAG prompts with strict context constraints to prevent hallucinations.
* Require the LLM to cite sources to make answers verifiable.

### Future Prevention
Configured automated test queries that evaluate response quality and source citations.

---

## 20. Engineering Lessons Summary

### Data Engineering
Tabular processing must be isolated from ingestion tasks. Validate formats early to ensure the data warehouse contains only clean, normalized records.

### System Architecture
Isolate ETL stages (Ingestion, Transformation, Storage, Retrieval) to make components modular and maintainable. This allows changing ingestion formats without updating the database layer.

### Cloud Deployment
Configure CORS whitelists and environment settings for each target environment. Cache dependencies and models to prevent deployment build failures and resource issues.

### REST APIs
Define strict Pydantic schemas for request/response validation. Enforce timezone-aware datetimes and fail-fast validation checks to improve API stability.

### Frontend Architecture
Decouple state variables in complex analytical dashboards to prevent redundant re-renders and improve page loading performance.

### AI Integration
Format retrieved context as clean key-value pairs instead of raw text blocks to minimize token usage and improve answer accuracy. Apply similarity score thresholds to filter out irrelevant context.

### Database Design
Always enforce unique constraints on relational keys. Use upsert operations to prevent duplicate records during batch data loads.

---

## Engineering Timeline

```text
  Raw Excel Ingestion Failure
               │
               ▼
   [Developer Investigation] (Identify NaN / Timestamp errors)
               │
               ▼
   [Code Correction & Patch] (Add ISO format & Nan filters)
               │
               ▼
   [Local Pipeline Verification] (Verify row loaders and APIs)
               │
               ▼
   [Cloud Host Deployment] (Render backend update & CORS whitelist)
```

---

## Recurring Debugging Workflow

### 1. Observe
Monitor logs to capture errors, warning outputs, and trace statements.

### 2. Reproduce
Create local test environments to reproduce the reported bug using the same parameters.

### 3. Isolate
Trace inputs through pipeline layers (Ingestion, Transformation, Storage) to isolate the failing module.

### 4. Inspect
Use debuggers or trace outputs to check values, cell formats, and datatypes at the module boundaries.

### 5. Patch
Implement the fix in the isolated module and run regression tests.

### 6. Verify
Verify the fix by running integration tests and checking database state changes.

### 7. Deploy
Deploy the changes to staging/production and monitor logs to ensure the issue is resolved.

---

## Best Practices Learned

### Ingestion & Normalization
* Always normalize business metrics using a centralized catalog mapping.
* Never use loose substring lookups for entity matching.
* Forward-fill merged cells programmatically during ingestion.
* Read calculated cell values instead of raw Excel formulas.
* Ignore hidden sheets and empty rows early in the pipeline.

### Data Warehousing
* Always enforce unique constraints on relational keys.
* Prefer upsert operations over insert queries for batch loads.
* Use JSONB fields to store variable-length time-series data.
* Standardize temporal properties to ISO-8601 strings.
* Set indices on fields used for filtering and search queries.

### API Architecture
* Never hardcode API endpoints in frontend client configurations.
* Use environment variables to configure URLs across development environments.
* Define strict Pydantic schemas for request/response validation.
* Separate read and write database client credentials.
* Implement CORS whitelists for all deployment environments.
* Enforce timezone-aware UTC datetime values.

### Frontend Design
* Decouple state variables to prevent redundant component re-renders.
* Sort and format datasets on the client side to prevent chart rendering errors.
* Use lightweight charting libraries for real-time visualization.
* Enforce runtime environment checks before API requests.

### AI & Retrieval
* Cache generated embeddings to prevent runtime regeneration latency.
* Format retrieved context as clean key-value pairs to improve accuracy.
* Apply strict distance thresholds to vector query matches.
* Constrain LLM responses to retrieved context to prevent hallucinations.
* Require the LLM to cite sources to make answers verifiable.
