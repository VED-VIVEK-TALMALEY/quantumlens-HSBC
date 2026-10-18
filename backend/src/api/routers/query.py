## -------------------------------------------------------------------
## Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
## This project and its source code are strictly proprietary.
## Unauthorized copying, distribution, or use is strictly prohibited.
## -------------------------------------------------------------------

from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.agents.orchestrator import get_orchestrator

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None


@router.post("/query")
def query(request: QueryRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )
    try:
        orchestrator = get_orchestrator()
        result = orchestrator.execute(
            question=question,
            conversation_id=request.conversation_id,
        )
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))