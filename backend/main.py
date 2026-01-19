"""
FastAPI backend for Mini RAG application.
Endpoints: POST /ingest, POST /query
"""

import time
from typing import Optional, List

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader
from io import BytesIO

# MUST be first executable line
load_dotenv()

from rag.chunking import SentenceAwareChunker
from rag.embeddings import EmbeddingGenerator
from rag.vectorstore import QdrantVectorStore
from rag.retriever import MMRRetriever
from rag.reranker import CohereReranker
from rag.qa import QAGenerator
import os


# ---------- APP ----------
app = FastAPI(title="Mini RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mini-rag-azure.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- COMPONENTS ----------
embedding_generator = EmbeddingGenerator()
vectorstore = QdrantVectorStore(recreate=True)
retriever = MMRRetriever(vectorstore, embedding_generator, k=8)
reranker = CohereReranker(top_n=4)
qa_generator = QAGenerator()
chunker = SentenceAwareChunker(
    min_tokens=800,
    max_tokens=1200,
    overlap_ratio=0.12
)

print("✓ All components initialized successfully")


# ---------- SCHEMAS ----------
class QueryRequest(BaseModel):
    q: str


class Citation(BaseModel):
    number: int
    source: str
    section: str
    position: int
    excerpt: str


class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    metrics: dict


class IngestResponse(BaseModel):
    count: int
    collection_name: str


# ---------- ROUTES ----------
@app.get("/")
async def root():
    return {"status": "ok", "message": "Mini RAG API"}


@app.post("/ingest", response_model=IngestResponse)
async def ingest(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    source: str = Form("upload"),
    title: Optional[str] = Form(None),
    section: str = Form("main"),
):
    if not title or title.lower() in {"document", "unknown"}:
        if file:
            title = os.path.splitext(file.filename)[0]
        else:
            title = source

    if not text and not file:
        raise HTTPException(status_code=400, detail="Text or file required")

    if text:
        content = text.strip()
    else:
        raw = await file.read()

        if file.filename.lower().endswith(".pdf"):
            reader = PdfReader(BytesIO(raw))
            content = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            content = raw.decode("utf-8", errors="ignore")

    if not content.strip():
        raise HTTPException(status_code=400, detail="Empty content")

    chunks = chunker.chunk(
        text=content,
        source=source,
        title=title,
        section=section,
    )

    texts = [c["text"] for c in chunks]
    embeddings = embedding_generator.embed(texts, mode="document")

    count = vectorstore.upsert_chunks(chunks, embeddings)

    return IngestResponse(
        count=count,
        collection_name=vectorstore.collection_name,
    )


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    start_time = time.perf_counter()

    retrieved = retriever.retrieve(request.q)

    # ---- No-answer case ----
    if not retrieved:
        return QueryResponse(
            answer="No relevant information found in the provided documents.",
            citations=[],
            sources=[],
            metrics={
                "latency_ms": 0.0,
                "token_estimate": 0,
                "retrieved_chunks": 0,
            },
            retrieved_ids=[],
        )

    # ---- Normal flow ----
    reranked = reranker.rerank(request.q, retrieved)
    qa_result = qa_generator.generate_answer(request.q, reranked)

    latency_ms = (time.perf_counter() - start_time) * 1000

    # token estimate based on answer length (acceptable for assessment)
    token_estimate = int(len(qa_result["answer"].split()) * 1.3)

    return QueryResponse(
        answer=qa_result["answer"],
        citations=qa_result["citations"],
        sources=qa_result["sources"],
        metrics={
            "latency_ms": round(latency_ms, 2),
            "token_estimate": token_estimate,
            "retrieved_chunks": len(reranked),
        },
        retrieved_ids=[c.get("id") for c in reranked],
    )

# ---------- ENTRY ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
