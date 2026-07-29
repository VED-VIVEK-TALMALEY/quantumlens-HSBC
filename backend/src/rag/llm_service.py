# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from groq import Groq
from src.config.settings import settings

client = Groq(
    api_key=settings.GROQ_API_KEY
)


def generate_answer(prompt):

    response = client.chat.completions.create(

        model=settings.LLM_MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS

    )

    return response.choices[0].message.content