## -------------------------------------------------------------------
## Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
## This project and its source code are strictly proprietary.
## Unauthorized copying, distribution, or use is strictly prohibited.
## -------------------------------------------------------------------


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.agents.orchestrator import Orchestrator

router = APIRouter()

orchestrator = Orchestrator()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        result = orchestrator.execute(
            request.question
        )
        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )