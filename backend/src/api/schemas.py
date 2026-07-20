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