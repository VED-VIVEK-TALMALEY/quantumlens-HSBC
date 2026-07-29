# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from pydantic import BaseModel
from typing import List, Dict, Any


class QuestionRequest(BaseModel):

    question: str


class SearchRequest(BaseModel):

    query: str

    top_k: int = 5


class AskResponse(BaseModel):

    question: str

    answer: str

    sources: List[Dict[str, Any]]