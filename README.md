# Mini RAG Application

A production-ready Retrieval-Augmented Generation (RAG) system built with Qdrant Cloud, Cohere embeddings and reranking, and Groq LLaMA-3.1-8B for answer generation.

##  Architecture

```
┌─────────────┐
│   Frontend  │  Next.js (Vercel)
│  (Next.js)  │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────┐
│   Backend   │  FastAPI (Render)
│  (FastAPI)  │
└──────┬──────┘
       │
       ├──► Cohere API (Embeddings: 1024-D)
       ├──► Qdrant Cloud (Vector DB: mini_rag_docs)
       ├──► Cohere API (Rerank v3)
       └──► Groq (LLaMA-3.1-8B)
```

### Data Flow

1. **Ingestion Flow:**
   ```
   Document → Chunking (800-1200 tokens, 12% overlap) 
           → Embedding (Cohere embedding-3-large, 1024-D)
           → Qdrant Cloud (cosine similarity)
   ```

2. **Query Flow:**
   ```
   Query → Embed Query → Vector Search (k=8) 
        → Rerank (Cohere, top 3-4) 
        → LLM Answer (groq cloud, with citations)
        → Response (answer + citations + sources)
   ```

## Features

- **Sentence-aware chunking** with configurable size and overlap
- **High-dimensional embeddings** (1024-D) for semantic search
- **MMR retrieval** for diverse, relevant results
- **Reranking** for improved precision
- **Strict grounding** - LLM only uses retrieved chunks
- **Inline citations** with source tracking
- **No-answer handling** when information is unavailable

## Chunking Parameters

### Configuration
- **Size Range:** 800-1200 tokens per chunk
- **Overlap:** 12% (middle of 10-15% range)
- **Method:** Sentence-aware (preserves sentence boundaries)

### Rationale
- **800-1200 tokens:** Balances context completeness with retrieval precision. Too small = fragmented context, too large = noisy retrieval.
- **12% overlap:** Ensures continuity across chunk boundaries, preventing information loss at edges.
- **Sentence-aware:** Preserves semantic units, improving embedding quality and readability.

### Metadata Stored
- `source`: Document identifier (filename, URL, etc.)
- `title`: Document title
- `section`: Section identifier
- `position`: Chunk position within document
- `token_count`: Token count for the chunk

## Vector Database Schema

### Qdrant Cloud Configuration
- **Collection Name:** `mini_rag_docs`
- **Dimension:** 1024 (matches Cohere Embeddings)
- **Distance Metric:** Cosine similarity
- **Upsert Strategy:** Hash-based ID generation from `source_position` to handle updates

### Payload Schema
```json
{
  "text": "chunk text content",
  "source": "document identifier",
  "section": "section name",
  "position": 0,
  "token_count": 950
}
```

## Retriever & Reranker Configuration

### Retriever (MMR)
- **Initial k:** 8 chunks
- **Method:** Cosine similarity search in Qdrant
- **Purpose:** Retrieve diverse, relevant candidates for reranking

### Reranker (Cohere)
- **Model:** `rerank-english-v3.0`
- **Top N:** 4 chunks (final selection)
- **Purpose:** Improve precision by reranking based on query relevance

### Rationale
- **k=8 initial retrieval:** Provides enough candidates for reranker to select from while maintaining diversity.
- **Top 4 final chunks:** Balances context window limits with answer completeness. 4 chunks (~4000 tokens) provide sufficient context for most questions.

## Providers & Environment Variables

### Required Services
1. **Groq cloud** - LLM (LLaMA-3.1-8B)
2. **Qdrant Cloud** - Vector database hosting
3. **Cohere** - Embedding and Reranking service


## Deployment

### Backend (Render)

#### Option 1: Render
1. Create new Web Service on Render
2. Connect GitHub repository
3. Set build command: `cd backend && pip install -r requirements.txt`
4. Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard
6. Deploy
`

### Frontend (Vercel)

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variable: `NEXT_PUBLIC_API_URL` = your backend URL
4. Deploy


### Live URLs
- **Backend:** https://mini-rag-4b08.onrender.com
- **Frontend:** https://mini-rag-azure.vercel.app/

##  Installation & Local Development

### Prerequisites
- Python 3.9+
- Node.js 18+
- API keys for Groq, Qdrant Cloud, and Cohere

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Edit .env with your API keys
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with backend URL
npm run dev
```


## 📊 Evaluation

### Gold Q/A Pairs
See `gold_qa_pairs.md` for 5 test questions and expected answers.

### Metrics
- **Precision:** >80% for factual questions, >70% for multi-part
- **Recall:** >75% for single-concept, >60% for multi-chunk
- **Answer Quality:** Grounded in retrieved chunks, accurate citations, no hallucinations

### Test Results
After ingesting the test document and running the gold Q/A pairs:
- Q1 (RAG definition): High precision, single chunk retrieval
- Q2 (Vector DBs): Medium precision, may need chunk combination
- Q3 (RAG pipeline): High recall needed, should capture all steps
- Q4 (ML/DL relationship): Medium recall, multi-chunk synthesis
- Q5 (Vector DB names): High precision, exact match required

## ⚠️ Limitations & Tradeoffs

### Current Limitations
1. **Simple MMR:** Uses top-k retrieval; true MMR diversity not fully implemented
2. **No PDF parsing:** File uploads expect text files only
3. **Fixed chunk size:** Doesn't adapt to document structure
4. **Single collection:** All documents in one Qdrant collection
5. **No authentication:** API endpoints are public

### Tradeoffs
- **Chunk size (800-1200):** Larger chunks = more context but lower precision
- **Overlap (12%):** More overlap = better continuity but more storage
- **k=8, top-4:** More candidates = better recall but higher latency
- **3072-D embeddings:** Higher quality but more storage/compute

### What's Next
1. **True MMR implementation** with diversity scoring
2. **PDF/document parsing** (PyPDF2, docx, etc.)
3. **Adaptive chunking** based on document structure
4. **Multi-collection support** for document organization
5. **Authentication/authorization** for production use
6. **Caching layer** for frequent queries
7. **Streaming responses** for better UX
8. **Evaluation framework** with automated metrics
9. **Hybrid search** (keyword + semantic)
10. **Query expansion** for better retrieval

## 📁 Project Structure

```
mini-rag/
├── backend/
│   ├── main.py                 # FastAPI app with /ingest and /query endpoints
│   ├── rag/
│   │   ├── chunking.py         # Sentence-aware chunking
│   │   ├── embeddings.py       # Cohere embeddings
│   │   ├── vectorstore.py      # Qdrant integration
│   │   ├── retriever.py        # MMR retriever (k=8)
│   │   ├── reranker.py         # Cohere reranker (top 3-4)
│   │   └── qa.py               # LLM answer generation with citations
│   ├── requirements.txt        # Python dependencies
│   └── env.example             # Environment variables template
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Main page
│   │   ├── components/
│   │   │   ├── UploadSection.tsx
│   │   │   ├── QuerySection.tsx
│   │   │   └── AnswerSection.tsx
│   │   └── globals.css         # Styles
│   ├── package.json
│   └── next.config.js
├── evaluation.md               # 5 Q/A pairs for obtaining performance metrics
└── README.md                   # This file
```


## Security Notes

- **API keys:** Stored server-side only (backend `.env`)
- **CORS:** Configured for frontend domain (update in production)
- **No secrets in frontend:** All API calls go through backend
- **Input validation:** FastAPI validates request formats

## License

MIT License - feel free to use and modify.

---

**Built with:** FastAPI, Next.js, Qdrant Cloud, Groq, Cohere
