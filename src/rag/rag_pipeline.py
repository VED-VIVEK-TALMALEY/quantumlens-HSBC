import time # Added missing import
from src.rag.retrieval_engine import RetrievalEngine
from src.rag.prompt_builder import build_prompt
from src.rag.llm_service import ask_llm
from src.rag.response_parser import parse_response
from src.config.settings import settings
from src.utils.logger import logger

engine = RetrievalEngine()

def ask(question):
    start = time.time()
    
    logger.info(f"Question : {question}")
    
    retrieval = engine.search(
        question,
        top_k=settings.TOP_K
    )
    retrieval_end = time.time()
    
    logger.info(f"Retrieval took {retrieval_end-start:.3f}s")
    
    prompt = build_prompt(
    question,
    retrieval["documents"][0]
)
    answer = ask_llm(prompt)
    llm_end = time.time()
    logger.info(
    f"LLM took "
    f"{llm_end - retrieval_end:.3f}s"
)
    logger.info(
    f"Total "
    f"{llm_end - start:.3f}s"
    )
    return parse_response( # Corrected indentation
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