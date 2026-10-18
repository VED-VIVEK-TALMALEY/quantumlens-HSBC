# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[Dict[str, Any]]