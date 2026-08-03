# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from .execution_context import ExecutionContext
from src.rag.prompt_builder import build_prompt
from src.rag.llm_service import generate_answer


class LLMAgent:

    def execute(self, context: ExecutionContext):

        prompt = build_prompt(

            context.question,

            context.sql_result,

            context.rag_result

        )

        context.llm_result = generate_answer(prompt)

        return context


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    from .planner import Planner

    planner = Planner()

    plan = planner.plan("Why did CET1 fall?")

    context = ExecutionContext(

        question="Why did CET1 fall?",

        plan=plan,

        sql_result=[
            ("Period 1", 123996),
            ("Period 2", 132593)
        ],

        rag_result=[
            {
                "text": "CET1 is a regulatory capital ratio."
            }
        ]

    )

    agent = LLMAgent()

    context = agent.execute(context)

    print(context.llm_result)