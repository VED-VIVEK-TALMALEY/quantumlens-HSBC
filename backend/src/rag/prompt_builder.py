# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# Prompt Builder
# -------------------------------------------------------------------

class PromptBuilder:

    def build(
        self,
        question,
        sql_context,
        rag_context
    ):

        return f"""
You are QuantumLens.

You are a financial analyst.

Use ONLY the supplied context.

If the answer cannot be derived from the context,
say so.

Question
--------
{question}

SQL Context
-----------
{sql_context}

Retrieved Context
-----------------
{rag_context}

Instructions

- Never hallucinate.
- Use SQL values as primary evidence.
- Use RAG only for explanations.
- Mention numbers whenever possible.
- Keep the answer concise.
"""

_builder = PromptBuilder()


def build_prompt(question, sql_context, rag_context):
    return _builder.build(
        question,
        sql_context,
        rag_context
    )