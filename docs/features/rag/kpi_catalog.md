# KPI Catalog & Normalization Logic

This document details the metric normalization engine, lookup dictionary catalog entries, and target mapping strategies utilized by **QuantumLens**.

For system architecture layouts, see [architecture.md](../../architecture/architecture.md). For table details, see [data_dictionary.md](../ingestion/data_dictionary.md).

---

## The Normalization Engine

In financial analytics, different business sheets and reporting periods frequently reference the same underlying metric using distinct labels. For example, "Net Interest Income", "Net Interest", and "NII" refer to the same metric.

To handle this variation, the pipeline runs a string-standardization flow:

```text
  Raw Input Text               Clean & Normalize              Dictionary Hash Map             Normalized Output
" Net Interest Income " ──► "net interest income" ──► {"net interest income": ID: 1} ──► ID: 1, net_interest_income
```

### Ingestion Matching Workflow Table
| Step | Phase | Action | System Method | Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Cell Extraction | Read row list values from raw pandas structures. | `pandas.read_excel()` | `O(1)` |
| **2** | Normalization | Strip margins, cast strings to lowercase, trim spaces, and replace punctuation. | String cleanup regex | `O(M)` (M is string length) |
| **3** | Dictionary Matching| Probe the dictionary cache hash-map using the clean token. | Hash map check against JSON keys | `O(1)` |
| **4** | Record Hydration | If matched, extract values, map period indexes, and build target KPI record. | JSON serialization & timestamping | `O(P)` (P is period count) |

---

## Complete Catalog Lookup Dictionary

The system loads mapping configurations from [metric_dictionary.json](../../../backend/src/ingestion/metric_dictionary.json). Below is the complete catalog:

| Metric ID | Normalized Canonical Name | Abbreviation Code | Target Worksheet Context / Description |
| :--- | :--- | :--- | :--- |
| **1** | `net_interest_income` | `nii` | Banking net yield / Group Income Statement |
| **2** | `net_fee_income` | `nfi` | Non-interest fees / Group Income Statement |
| **3** | `other_operating_income` | `ooi` | Miscellaneous operating streams |
| **4** | `net_operating_income` | `noi` | Total net revenue after ECL |
| **5** | `expected_credit_losses` | `ecl` | Credit risk impairments and charges |
| **6** | `total_operating_expenses` | `toe` | Overhead, administrative, and system costs |
| **7** | `profit_before_tax` | `pbt` | Core operating profit pre-taxation |
| **8** | `profit_after_tax` | `pat` | Net income after tax deductions |
| **9** | `profit_attributable_to_ordinary_shareholders` | `paos` | Net income available for ordinary equity |
| **10** | `return_on_average_equity` | `roae` | Profitability indicator relative to average equity |
| **11** | `return_on_average_tangible_equity` | `rote` | Profitability indicator relative to tangible equity |
| **12** | `earnings_per_share` | `eps` | Basic earnings allocated per ordinary share |
| **13** | `dividends_per_share` | `dps` | Declared dividends distributed per share |
| **14** | `total_assets` | `ta` | Aggregate banking books assets / Balance Sheet |
| **15** | `total_liabilities` | `tl` | Aggregate outstanding liabilities / Balance Sheet |
| **16** | `total_shareholders_equity` | `tse` | Net asset value of the banking group |
| **17** | `loans_and_advances_to_customers_net` | `lacn` | Net customer credit books / Balance Sheet |
| **18** | `customer_accounts` | `ca` | Total customer deposits / Balance Sheet |
| **19** | `risk_weighted_assets` | `rwa` | Assets weighted by risk multipliers / Basel capital |
| **20** | `common_equity_tier_1_capital` | `cet1` | High-quality regulatory capital capital base |
| **21** | `common_equity_tier_1_ratio` | `cet1r` | CET1 capital divided by total RWA |
| **22** | `tier_1_ratio` | `t1r` | Tier 1 capital divided by total RWA |
| **23** | `total_capital_ratio` | `tcr` | Total capital divided by total RWA |
| **24** | `leverage_ratio` | `lr` | Tier 1 capital divided by total leverage exposure |
| **25** | `net_interest_margin` | `nim` | Net interest income relative to earning assets |
| **26** | `tangible_net_asset_value` | `tnav` | Total equity excluding intangible assets |
| **27** | `net_asset_value_per_share` | `navps` | Net tangible assets allocated per share |
| **28** | `banking_net_interest_income` | `bnii` | Segmented commercial banking net interest yield |
| **29** | `wholesale_transaction_banking_revenue` | `wtbr` | Corporate banking transaction fees revenue |
| **30** | `wealth_revenue` | `wr` | Asset management and private banking revenues |
| **31** | `revenue` | `rev` | Top-line sales and revenues |
| **32** | `deposits` | `dep` | Customer deposits aggregate |
| **33** | `wealth_net_new_money` | `wnnm` | Assets under management net inflow indicators |
| **34** | `cost_efficiency_ratio` | `cer` | Operating expenses divided by operating income |
| **35** | `operating_expenses` | `opex` | General operating costs |
| **36** | `credit_loss_ratio` | `clr` | Expected credit losses relative to gross loans |

---

## Normalization Process Benefits

| Feature | Substring Matching (Legacy) | Catalog Hash-Lookup (Current) | Core Benefit |
| :--- | :--- | :--- | :--- |
| **Lookup Time** | `O(N)` (searches all variations) | `O(1)` (direct hash lookup) | Sub-millisecond parsing speed |
| **Duplicate Prevention** | High risk (nested labels) | Zero risk (regex/hash mapping) | High data integrity |
| **Maintenance** | Requires modifying python scripts | Requires modifying dictionary JSON | Code remains untouched when adding new metrics |
| **RAG Precision** | High hallucination rate | Context limited to canonical IDs | Exact numeric context matched for LLMs |

---

## Related Documentation
* [Primary Readme](../../../README.md): Project overview, installation scripts, API reference.
* [System Architecture Spec](../../architecture/architecture.md): Systems layers overview.
* [Database Schema (Data Dictionary)](../ingestion/data_dictionary.md): Detailed columns description, indices, and constraints.
