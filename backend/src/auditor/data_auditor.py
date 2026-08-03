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

        metric = rows[0][3]
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
            if row[3] != metric:
                warnings.append("Mixed metrics returned.")
                confidence -= 0.20
                valid = False
                
            periods_list.append(int(row[self.PERIOD_INDEX]))

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
            "confidence": confidence,
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

if __name__ == "__main__":
    auditor = DataAuditor()
    
    print(auditor.audit([]))
    
    print(auditor.audit([
        (1, 2, 3, "CET1", 5, 6, 7, 1, 100),
        (1, 2, 3, "CET1", 5, 6, 7, 2, 200),
        (1, 2, 3, "CET1", 5, 6, 7, 4, 400),
        (1, 2, 3, "CET1", 5, 6, 7, 5, 500),
    ]))