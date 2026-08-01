# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------


from src.rag.prompt_builder import build_prompt
from src.rag.llm_service import generate_answer


class LLMAgent:

    def execute(
        self,
        question,
        sql_result,
        rag_result
    ):

        prompt = build_prompt(
            question,
            sql_result,
            rag_result
        )

        llm_response = generate_answer(prompt)

        return llm_response


if __name__ == "__main__":

    agent = LLMAgent()

    result = agent.execute(

        question="Explain CET1 ratio",

        sql_result=[
            ("Period 1", 123996),
            ("Period 2", 132593)
        ],

        rag_result=[
            {
                "text":
                "CET1 is a regulatory capital ratio."
            }
        ]

    )

    print(result)