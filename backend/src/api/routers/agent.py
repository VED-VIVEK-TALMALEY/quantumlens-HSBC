# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
#
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.api.services.agent_service import process_question


router = APIRouter()


class AgentQuery(BaseModel):
    question: str


@router.post("/agent/query")
def agent_query(request: AgentQuery):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    return process_question(question)