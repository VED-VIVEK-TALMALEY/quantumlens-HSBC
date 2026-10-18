# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

class DataAuditor:
    VALUE_INDEX = 8
    PERIOD_INDEX = 7

    def audit(self, rows):
        if not rows:
            return {
                "valid": False,
                "confidence": 0.0,
                "warnings": ["No records returned."],
                "clean_rows": []
            }

        warnings = []
        confidence = 1.0
        valid = True

        first_row = rows[0]

        # Case 1: Supabase dictionary records with JSONB period_values
        if isinstance(first_row, dict):
            metric = first_row.get("metric_name") or first_row.get("abbreviation")

            for row in rows:
                row_metric = row.get("metric_name") or row.get("abbreviation")
                if row_metric != metric:
                    warnings.append(f"Mixed metrics returned: '{row_metric}' vs '{metric}'.")
                    confidence -= 0.20
                    valid = False

                periods = row.get("period_values")
                if not periods:
                    warnings.append(f"No period values found for row {row.get('row_number', '?')}.")
                    confidence -= 0.20
                    valid = False
                    continue

                period_indices = []
                for p in periods:
                    val = p.get("value")
                    idx = p.get("period_index")

                    if val is None:
                        warnings.append(f"Null value detected in period {idx}.")
                        confidence -= 0.15
                        valid = False

                    try:
                        if val is not None:
                            float(val)
                    except (TypeError, ValueError):
                        warnings.append(f"Non-numeric value in period {idx}: '{val}'")
                        confidence -= 0.20
                        valid = False

                    if idx is not None:
                        try:
                            period_indices.append(int(idx))
                        except (TypeError, ValueError):
                            pass

                if period_indices:
                    periods_set = set(period_indices)
                    if len(period_indices) != len(periods_set):
                        warnings.append("Duplicate periods detected.")
                        confidence -= 0.10
                        valid = False

        # Case 2: Legacy tuple records (e.g. SQLite / table rows)
        else:
            try:
                metric = first_row[3]
            except (IndexError, KeyError):
                metric = None

            periods_list = []
            for row in rows:
                # 1. Null values check
                if row[self.VALUE_INDEX] is None:
                    warnings.append("Null value detected.")
                    confidence -= 0.20
                    valid = False

                # 2. Numeric check
                try:
                    float(row[self.VALUE_INDEX])
                except IndexError:
                    warnings.append("Malformed SQL row.")
                    confidence -= 0.50
                    valid = False
                except (TypeError, ValueError):
                    warnings.append(f"Non-numeric value in period {row[self.PERIOD_INDEX]}")
                    confidence -= 0.30
                    valid = False

                # 3. Metric consistency check
                if len(row) > 3 and row[3] != metric:
                    warnings.append("Mixed metrics returned.")
                    confidence -= 0.20
                    valid = False

                if len(row) > self.PERIOD_INDEX and row[self.PERIOD_INDEX] is not None:
                    periods_list.append(int(row[self.PERIOD_INDEX]))

            if periods_list:
                periods_set = set(periods_list)
                expected = set(range(min(periods_set), max(periods_set) + 1))
                missing = expected - periods_set

                # 4. Missing periods check
                if missing:
                    warnings.append(f"Missing Period(s): {sorted(missing)}")
                    confidence -= 0.15
                    valid = False

                # 5. Duplicate periods check
                if len(periods_list) != len(periods_set):
                    warnings.append("Duplicate periods detected.")
                    confidence -= 0.10
                    valid = False

                # 6. Chronological order check
                if periods_list != sorted(periods_list):
                    warnings.append("Periods not in chronological order.")
                    confidence -= 0.10

        confidence = max(confidence, 0.0)

        return {
            "valid": valid,
            "confidence": round(confidence, 2),
            "warnings": warnings,
            "clean_rows": rows
        }

    def execute(self, context):
        audit = self.audit(
            context.sql_result
        )

        context.audit_result = audit

        if audit["valid"]:
            context.sql_result = audit["clean_rows"]

        return context