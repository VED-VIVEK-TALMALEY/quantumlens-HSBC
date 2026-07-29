# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

def build_prompt(
    question,
    retrieved_docs
):

    context = ""

    for doc in retrieved_docs:

        context += doc
        context += "\n\n"

    prompt = f"""
You are an HSBC Financial Copilot.

Rules:

1. Use ONLY the retrieved KPI records.
2. Never invent numbers.
3. Quote values exactly.
4. Mention workbook and sheet.
5. If unavailable, say so.
6. Explain trends if multiple values exist.
7. Format using bullet points.
{context}

Question

{question}

Answer
"""

    return prompt 