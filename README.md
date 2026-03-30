# IT Service Copilot (RAG)

Enterprise IT support assistant built with **Retrieval-Augmented Generation (RAG)**. Plain-text knowledge files are chunked, embedded with a Hugging Face model, stored in **Chroma**, and answers are generated with **Groq** (Llama 3.1) using only retrieved context.

**Remote:** [github.com/rav-stack/IT-Service-Copilot-rag](https://github.com/rav-stack/IT-Service-Copilot-rag)

## Features

- **FastAPI** `POST /ask` endpoint: accepts a question, retrieves top-k similar chunks, returns the model answer plus the retrieved text used as context.
- **Grounded answers**: The LLM is instructed to answer only from context; if nothing matches, it responds with *"Insufficient data to process an answer"*.
- **Configurable embeddings and vector DB** via environment variables (see below).

## Project layout

| Path | Role |
|------|------|
| `app/main.py` | FastAPI app and `/ask` route |
| `app/services/retrieval_service.py` | Similarity search over Chroma |
| `app/services/vectorstore_service.py` | Hugging Face embeddings + Chroma client |
| `app/services/ingest_service.py` | Load → chunk → index pipeline |
| `app/services/llm_service.py` | Groq chat completion |
| `app/utils/loaders.py` | Reads all `.txt` files from a folder |
| `app/utils/chunking.py` | `RecursiveCharacterTextSplitter` (500 / 50 overlap) |
| `scripts/ingest_data.py` | CLI entrypoint for ingestion |
| `data/raw/` | Example knowledge files (policies, troubleshooting notes) |

## Prerequisites

- Python 3.10+ (3.11 recommended)
- A [Groq](https://console.groq.com/) API key

## Setup

1. **Clone and enter the project**

   ```bash
   git clone https://github.com/rav-stack/IT-Service-Copilot-rag.git
   cd IT-Service-Copilot-rag
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Environment variables**

   Create a `.env` file in the project root (same folder as `requirements.txt`):

   ```env
   GROQ_API_KEY=your_groq_api_key
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   CHROMA_DB_DIR=./chroma_db
   ```

   - **`GROQ_API_KEY`**: Required for `/ask`.
   - **`EMBEDDING_MODEL`**: Any model name supported by [HuggingFaceEmbeddings](https://python.langchain.com/docs/integrations/text_embedding/huggingface_hub); the default above is small and fast. The first run may download model weights.
   - **`CHROMA_DB_DIR`**: Persistent directory for the Chroma store (created on first ingest).

## Ingest knowledge

From the project root, with the virtual environment active:

```bash
python -m scripts.ingest_data
```

This reads every file in `data/raw/`, splits into chunks, and upserts into Chroma under `CHROMA_DB_DIR`. Run again after adding or changing files in `data/raw/`.

## Run the API

```bash
uvicorn app.main:app --reload
```

Default URL: `http://127.0.0.1:8000`

### Example request

```bash
curl -s -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I request VPN access?"}'
```

Response shape:

```json
{
  "question": "...",
  "retrieved_documents": "...",
  "answer": "..."
}
```

Interactive docs: `http://127.0.0.1:8000/docs`

## Stack

- **API**: FastAPI, Uvicorn, Pydantic  
- **RAG**: LangChain (text splitters, Chroma integration, Hugging Face embeddings)  
- **Vector store**: Chroma (persistent on disk)  
- **LLM**: Groq — `llama-3.1-8b-instant`

## License

Add a `LICENSE` file in the repository if you want to specify terms for reuse.
