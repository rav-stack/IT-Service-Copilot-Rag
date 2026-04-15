from fastapi import FastAPI
import fastapi
from pydantic import BaseModel
from app.services.retrieval_service import retrieve_documents
from app.services.llm_service import generate_answer

app = FastAPI()

class QueryRequest(BaseModel):
    query: str


@app.post("/ask")
def ask_question(request: QueryRequest):
    docs = retrieve_documents(request.query)

    #context = "\n".join([doc.page_content for doc in docs]) 
    # #LLM hallucinated because source names because metadata was not propagated into the prompt.
    # the below function passess source name as well as the content of the chunk to the LLM

    context = "\n\n".join([f"Source : {doc.metadata.get('source')}\nContent:{doc.page_content}" for doc in docs])

    sources = list(set([doc.metadata.get("source","unknown") for doc in docs]))
    answer = generate_answer(request.query,context)
    
    return {
        "question" : request.query,
        "answer": answer,
        "sources" : sources
        
    }

#uvicorn app.main:app --reload
#python -m scripts.ingest_data