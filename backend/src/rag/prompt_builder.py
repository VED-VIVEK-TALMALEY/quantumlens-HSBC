# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# -------------------------------------------------------------------


class PromptBuilder:

    def build(
        self,
        question,
        sql_context,
        rag_context,
        financial_reasoning
    ):

        # -------------------------------------------------
        # SQL Context
        # -------------------------------------------------

        sql_text = ""

        if sql_context:

            for row in sql_context:

                sql_text += (
                    f"Metric={row[3]}, "
                    f"Period={row[7]}, "
                    f"Value={row[8]}\n"
                )

        else:

            sql_text = "No SQL data available."

        # -------------------------------------------------
        # Metric Knowledge
        # -------------------------------------------------

        metric_text = ""

        metric_docs = rag_context.get("metrics", [])

        for doc in metric_docs[:3]:

            metric_text += doc["text"] + "\n\n"

        if not metric_text:

            metric_text = "No metric documentation found."

        # -------------------------------------------------
        # Narrative Evidence
        # -------------------------------------------------

        narrative_text = ""

        narrative_docs = rag_context.get("documents", [])

        for doc in narrative_docs[:5]:

            page = doc["metadata"].get("page", "?")

            narrative_text += (
                f"[Page {page}]\n"
                f"{doc['text']}\n\n"
            )

        if not narrative_text:

            narrative_text = "No narrative evidence found."

        # -------------------------------------------------
        # Financial Reasoning
        # -------------------------------------------------

        reasoning_text = ""

        if financial_reasoning:

            for key, value in financial_reasoning.items():

                reasoning_text += f"{key}: {value}\n"

        else:

            reasoning_text = "No financial reasoning available."

        # -------------------------------------------------
        # Final Prompt
        # -------------------------------------------------

        prompt = f"""
You are QuantumLens, an expert financial analyst.

Use ONLY the evidence provided.

================================================
FINANCIAL REASONING
================================================

{reasoning_text}

================================================
SQL EVIDENCE
================================================

{sql_text}

================================================
METRIC KNOWLEDGE
================================================

{metric_text}

================================================
MANAGEMENT COMMENTARY
================================================

{narrative_text}

================================================
QUESTION
================================================

{question}

================================================
RULES
================================================

1. SQL values are the source of truth.
2. Financial reasoning summarizes the numerical evidence.
3. Narrative explains WHY something happened.
4. Never invent explanations.
5. If the disclosures do not explain something, explicitly say:
   "The available disclosures do not explain the reason."
6. Quote page numbers whenever possible.
7. Keep answers concise.
"""

        return prompt


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    builder = PromptBuilder()

    sql_rows = [

        ("", "", "", "cet1", "", "", "", "1", 123996),

        ("", "", "", "cet1", "", "", "", "2", 132593),

    ]

    rag = {

        "metrics": [

            {

                "text": "CET1 Ratio represents Common Equity Tier 1 Capital."

            }

        ],

        "documents": [

            {

                "text": "CET1 decreased due to strategic transactions.",

                "metadata": {

                    "page": 46

                }

            }

        ]

    }

    financial_reasoning = {

        "first_value": 123996,

        "last_value": 132593,

        "absolute_change": 8597,

        "percent_change": 6.93,

        "direction": "increase",

        "highest_period": "2",

        "lowest_period": "1",

        "trend": "upward"

    }

    print(

        builder.build(

            "Why did CET1 fall?",

            sql_rows,

            rag,

            financial_reasoning

        )

    )