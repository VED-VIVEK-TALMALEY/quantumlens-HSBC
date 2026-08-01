# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

def build_prompt(
    question,
    sql_result,
    rag_result
):

    prompt = f"""
You are an HSBC Financial Analyst.

Question:
{question}

SQL Data:
{sql_result}

Retrieved Context:
{rag_result}

Rules:

- Use SQL data as the primary source.
- Use retrieved context only for explanation.
- Never invent financial values.
- If data is missing, explicitly say so.

Provide a concise financial explanation.
"""

    return prompt