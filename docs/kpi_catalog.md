# 📋 KPI Catalog & Normalization Logic

This document details the metric normalization engine, lookup dictionary catalog entries, and target mapping strategies utilized by **QuantumLens**.

For system architecture layouts, see [architecture.md](architecture.md). For table details, see [data_dictionary.md](data_dictionary.md).

---

## ⚙️ The Normalization Engine

In financial analytics, different business sheets and reporting periods frequently reference the same underlying metric using distinct labels. For example, "Net Interest Income", "Net Interest", and "NII" refer to the same metric.

To handle this variation:
1. The **Ingestion Layer** scans all sheet rows.
2. Text values are extracted, lowercase-normalized, stripped of surrounding spaces, and run through a constant-time hashing dictionary match.
3. The matching row is converted to a normalized name (`net_interest_income`) and assigned a canonical identifier (`metric_id = 1`).

```text
  Raw Input Text               Clean & Normalize              Dictionary Hash Map             Normalized Output
" Net Interest Income " ──► "net interest income" ──► {"net interest income": ID: 1} ──► ID: 1, net_interest_income
```

---

## 📊 Catalog Lookup Dictionary

The system loads mapping configurations from [metric_dictionary.json](../src/config/metric_dictionary.json). Below is a structured snapshot of key catalog entries:

| Matched String Token (Key) | Metric ID | Normalized Canonical Name | Abbreviation Code | Target Worksheet Context |
| :--- | :--- | :--- | :--- | :--- |
| `net interest income` | `1` | `net_interest_income` | `nii` | Group Income Statement |
| `net fee income` | `2` | `net_fee_income` | `nfi` | Group Income Statement |
| `operating income` | `3` | `operating_income` | `oi` | Group Income Statement |
| `operating expenses` | `4` | `operating_expenses` | `opex` | Group Income Statement |
| `credit risk` | `5` | `credit_risk` | `cr` | Credit Risk / Balance Sheet |
| `customer accounts` | `6` | `customer_accounts` | `ca` | Balance Sheet |
| `loans and advances` | `7` | `loans_and_advances` | `la` | Balance Sheet |
| `total assets` | `8` | `total_assets` | `ta` | Balance Sheet |
| `total equity` | `9` | `total_equity` | `te` | Balance Sheet |
| `return on equity` | `10` | `return_on_equity` | `roe` | Financial Ratios |

---

## 🔄 Mapping Strategy

### Ingestion Matching Workflow

The loader executes the following matching flow for every row parsed in a workbook:

| Step | Action Name | Execution Detail | Complexity |
| :--- | :--- | :--- | :--- |
| **1** | Cell Extraction | Read row list values from raw pandas structures. | `O(1)` |
| **2** | Normalization | Strip margins, cast strings to lowercase, replace punctuation. | `O(M)` where M is string length |
| **3** | Dictionary Matching | Probe the dictionary cache hash-map using the clean token. | `O(1)` |
| **4** | Record Hydration | If matched, extract values, map period indexes, and build target KPI record. | `O(P)` where P is period count |

---

## 💡 Key Benefits of Centralized Normalization

| Benefit | Description |
| :--- | :--- |
| **O(1) Constant-Time Lookup** | Matching is optimized via Python dictionaries, allowing fast processing of thousands of workbook lines. |
| **Data Integrity** | Enforces consistent naming rules, resolving inconsistencies between quarters. |
| **Simple Scalability** | New metrics and abbreviations can be added directly to the configuration JSON without modifying python logic. |
| **Unified Cohort Comparison** | Downstream RAG agents can aggregate historical periods across years, even if sheets rename rows. |

---

## 🔗 Related Documentation
- [Primary Readme](../README.md): Project overview, installation scripts, API reference.
- [System Architecture Spec](architecture.md): Systems layers overview and Mermaid diagrams.
- [Database Schema (Data Dictionary)](data_dictionary.md): Detailed columns description, indices, and constraints.
