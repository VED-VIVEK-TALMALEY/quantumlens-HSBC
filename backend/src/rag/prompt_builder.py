# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# -------------------------------------------------------------------


class PromptBuilder:

    def build(
        self,
        question,
        sql_rows,
        rag_result
    ):

        # -----------------------------------------
        # SQL Context
        # -----------------------------------------

        sql_text = ""

        if sql_rows:

            for row in sql_rows:

                sql_text += (

                    f"Metric={row[3]}, "

                    f"Period={row[7]}, "

                    f"Value={row[8]}\n"

                )

        else:

            sql_text = "No SQL data available."

        # -----------------------------------------
        # Metric Knowledge
        # -----------------------------------------

        metric_text = ""

        metric_docs = rag_result.get("metrics", [])

        for doc in metric_docs[:3]:

            metric_text += doc["text"] + "\n\n"

        if metric_text == "":

            metric_text = "No metric documentation found."

        # -----------------------------------------
        # Narrative Evidence
        # -----------------------------------------

        narrative_text = ""

        narrative_docs = rag_result.get("documents", [])

        for doc in narrative_docs[:5]:

            page = doc["metadata"].get("page", "?")

            narrative_text += (

                f"[Page {page}]\n"

                f"{doc['text']}\n\n"

            )

        if narrative_text == "":

            narrative_text = "No narrative evidence found."

        # -----------------------------------------
        # Final Prompt
        # -----------------------------------------

        prompt = f"""
You are QuantumLens, an expert financial analyst.

Use ONLY the evidence provided.

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

2. Narrative explains WHY something happened.

3. Never invent explanations.

4. If no explanation exists,
say:
"The available disclosures do not explain the reason."

5. Quote page numbers whenever possible.

6. Keep answers concise.

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

                "text":

                "CET1 decreased due to strategic transactions.",

                "metadata":

                {

                    "page": 46

                }

            }

        ]

    }

    print(

        builder.build(

            "Why did CET1 fall?",

            sql_rows,

            rag

        )

    )