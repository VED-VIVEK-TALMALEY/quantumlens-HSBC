# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import time

from src.rag.engine import get_engine
from src.rag.prompt_builder import build_prompt
from src.rag.llm_service import generate_answer
from src.rag.response_parser import parse_response
from src.config.settings import settings
from src.utils.logger import logger

engine = get_engine()

def ask(question):
    start = time.time()
    
    logger.info(f"Question : {question}")
    
    retrieval = engine.search(
        question,
        top_k=settings.TOP_K
    )
    retrieval_end = time.time()
    
    logger.info(f"Retrieval took {retrieval_end-start:.3f}s")
    
    context = [
        doc["text"]
        for doc in retrieval
    ]

    prompt = build_prompt(
        question,
        context
    )
    
    answer = generate_answer(prompt)
    llm_end = time.time()
    
    logger.info(f"LLM took {llm_end - retrieval_end:.3f}s")
    logger.info(f"Total {llm_end - start:.3f}s")
    
    return parse_response(
        question,
        answer,
        retrieval
    )

if __name__ == "__main__":
    while True:
        q = input("\nQuestion: ")
        if q.lower() == "exit":
            break
            
        result = ask(q)
        
        print("\nAnswer\n")
        print(result["answer"])