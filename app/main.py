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

    relevant_docs = "\n".join([obj.page_content for obj in docs])
    answer = generate_answer(request.query,relevant_docs)
    
    return {
        "question" : request.query,
        "retrieved_documents" : relevant_docs,
        "answer": answer
    }

#uvicorn app.main:app --reload
#python -m scripts.ingest_data