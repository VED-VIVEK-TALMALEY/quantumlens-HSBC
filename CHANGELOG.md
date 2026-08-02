<!-- -------------------------------------------------------------------
Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
This project and its source code are strictly proprietary.
Unauthorized copying, distribution, or use is strictly prohibited.
------------------------------------------------------------------- -->

# Changelog

All notable changes to the **QuantumLens** platform are documented in this file.

---

## [1.0.0] - 2026-03-10

### Release Status
| Attribute | Details |
| :--- | :--- |
| **Milestone** | Production Ready / Stable Release |
| **Primary Target** | Full Pipeline Integration (FastAPI + Next.js + Dual-Database) |
| **Stability** | Release Candidate Approved |

### Detailed Change History

| Date | Category | Description | Severity/Impact | Issues Addressed |
| :--- | :--- | :--- | :--- | :--- |
| **2026-03-05** | AI Layer | Refactored RAG system prompts to restrict answers to factual context with workbook citations. | High | [Issue #19](docs/refactoring/issues.md#19-ai-assistant-development) |
| **2026-02-28** | Frontend UI | Decoupled React state object into specific hooks (`selectedMetric`, `selectedRecord`). | Medium | [Issue #18](docs/refactoring/issues.md#18-frontend-state-management) |
| **2026-02-25** | Frontend UI | Implemented client-side chronological sorting of datasets for Recharts. | Medium | [Issue #17](docs/refactoring/issues.md#17-chart-rendering-problems) |
| **2026-02-22** | Integration | Configured environment variables (`NEXT_PUBLIC_API_URL`) to replace hardcoded endpoints. | High | [Issue #16](docs/refactoring/issues.md#16-localhost-vs-production-api) |
| **2026-02-20** | Deployment | Added missing production dependencies (`uvicorn`, `gunicorn`) and optimized RAM consumption. | High | [Issue #15](docs/refactoring/issues.md#15-render-deployment-issues) |
| **2026-02-18** | Deployment | Configured Vercel build configs to target `frontend/` as root. | Medium | [Issue #14](docs/refactoring/issues.md#14-vercel-framework-detection) |
| **2026-02-15** | Configuration | Added `python-dotenv` support and defined default fallback variables for API server setup. | High | [Issue #15](docs/refactoring/issues.md#15-render-deployment-issues) |
| **2026-02-12** | Cloud Deployment| Configured FastAPI CORS middleware to whitelist the Next.js Vercel URL. | Critical | [Issue #12](docs/refactoring/issues.md#12-cors-deployment-failure) |
| **2026-02-08** | AI Layer | Refactored RAG pipeline context formatting to clean key-value structures. | High | [Issue #11](docs/refactoring/issues.md#11-rag-quality-problems) |
| **2026-02-05** | AI Layer | Configured ChromaDB persistence path inside the workspace and cached vector embeddings. | Medium | [Issue #10](docs/refactoring/issues.md#10-chromadb-integration) |
| **2026-02-02** | Ingestion | Programmed formula value execution and forward-fill logic for merged header cells. | High | [Issue #9](docs/refactoring/issues.md#9-excel-ingestion-parsing-issues) |
| **2026-01-28** | Transformation| Introduced `period_mapper.py` to assign sequential database period IDs to numerical columns. | Medium | [Issue #8](docs/refactoring/issues.md#8-period-mapping-challenges) |
| **2026-01-25** | Ingestion | Added regex boundary constraints to `metric_extractor.py` to prevent nested label matches. | High | [Issue #7](docs/refactoring/issues.md#7-kpi-extraction-errors) |
| **2026-01-22** | Runtime | Replaced deprecated `datetime.utcnow()` with timezone-aware `datetime.now(timezone.utc)`. | Low | [Issue #6](docs/refactoring/issues.md#6-datetime-utc-deprecation) |
| **2026-01-20** | Security | Switched database write connections to use the Supabase administrative Service Key. | Critical | [Issue #5](docs/refactoring/issues.md#5-supabase-authentication-issues) |
| **2026-01-18** | Data Layer | Configured PostgreSQL schema with `UNIQUE` constraint and switched to `.upsert()`. | High | [Issue #4](docs/refactoring/issues.md#4-duplicate-database-records) |
| **2026-01-15** | Transformation| Created centralized mapping `metric_dictionary.json` hash map lookup catalog. | Medium | [Issue #3](docs/refactoring/issues.md#3-metric-normalization-problems) |
| **2026-01-12** | Ingestion | Replaced NumPy floating-point `NaN` parameters with Python `None` values. | High | [Issue #2](docs/refactoring/issues.md#2-nan-values-breaking-json) |
| **2026-01-10** | API | Converted `Timestamp` data formats to ISO-8601 strings to prevent serialization errors. | High | [Issue #1](docs/refactoring/issues.md#1-json-serialization-failure) |

---
## v5.0.0 - Multi-Agent Intelligence

### Added
- LLM Agent integrated into the orchestration pipeline
- Conversation Memory for contextual follow-up queries
- Agent Registry for centralized agent management
- Planner support for LLM execution (`needs_llm`)
- Response Agent support for LLM-generated answers

### Improved
- Orchestrator now supports memory-aware query resolution
- Analysis queries now combine SQL + RAG + LLM
- Cleaner separation between reasoning and response generation

### Current Architecture
Planner
→ Agent Registry
→ SQL Agent
→ Data Auditor
→ Chart Agent
→ RAG Agent
→ LLM Agent
→ Response Agent