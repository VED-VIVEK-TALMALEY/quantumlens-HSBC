# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------


from src.rag.prompt_builder import PromptBuilder
from src.rag.llm_service import generate_answer

builder = PromptBuilder()


class LLMAgent:

    def execute(self, context):

        prompt = builder.build(
            context.question,
            context.sql_result,
            context.rag_result
        )

        response = generate_answer(prompt)

        context.llm_result = response

        return context


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    from .execution_context import ExecutionContext
    from .planner import Planner

    planner = Planner()

    plan = planner.plan("Why did CET1 fall?")

    context = ExecutionContext(
        question="Why did CET1 fall?",
        plan=plan,
        sql_result=[
            (91, 20, "common_equity_tier_1_capital", "cet1", "", "", "", "1", 123996),
            (92, 20, "common_equity_tier_1_capital", "cet1", "", "", "", "2", 132593),
        ],
        rag_result=[
            {
                "text": "CET1 decreased mainly due to strategic transactions."
            }
        ]
    )

    agent = LLMAgent()

    context = agent.execute(context)

    print(context.llm_result)