# Mini RAG Application

A production-ready Retrieval-Augmented Generation (RAG) system built with Qdrant Cloud, OpenAI embeddings, Cohere reranking, and GPT-4o-mini for answer generation.

## 🏗️ Architecture

```
┌─────────────┐
│   Frontend  │  Next.js (Vercel)
│  (Next.js)  │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────┐
│   Backend   │  FastAPI (Render/Fly.io)
│  (FastAPI)  │
└──────┬──────┘
       │
       ├──► OpenAI API (Embeddings: text-embedding-3-large)
       ├──► Qdrant Cloud (Vector DB: mini_rag_docs)
       ├──► Cohere API (Rerank v3)
       └──► OpenAI API (LLM: gpt-4o-mini)
```

### Data Flow

1. **Ingestion Flow:**
   ```
   Document → Chunking (800-1200 tokens, 12% overlap) 
           → Embedding (OpenAI text-embedding-3-large, 3072-D)
           → Qdrant Cloud (cosine similarity)
   ```

2. **Query Flow:**
   ```
   Query → Embed Query → Vector Search (k=8) 
        → Rerank (Cohere, top 3-4) 
        → LLM Answer (gpt-4o-mini, with citations)
        → Response (answer + citations + sources)
   ```

## 📋 Features

- **Sentence-aware chunking** with configurable size and overlap
- **High-dimensional embeddings** (3072-D) for semantic search
- **MMR retrieval** for diverse, relevant results
- **Reranking** for improved precision
- **Strict grounding** - LLM only uses retrieved chunks
- **Inline citations** with source tracking
- **No-answer handling** when information is unavailable

## 🔧 Chunking Parameters

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

## 🗄️ Vector Database Schema

### Qdrant Cloud Configuration
- **Collection Name:** `mini_rag_docs`
- **Dimension:** 3072 (matches OpenAI text-embedding-3-large)
- **Distance Metric:** Cosine similarity
- **Upsert Strategy:** Hash-based ID generation from `source_position` to handle updates

### Payload Schema
```json
{
  "text": "chunk text content",
  "source": "document identifier",
  "title": "document title",
  "section": "section name",
  "position": 0,
  "token_count": 950
}
```

## 🔍 Retriever & Reranker Configuration

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

## 🔑 Providers & Environment Variables

### Required Services
1. **OpenAI** - Embeddings (text-embedding-3-large) and LLM (gpt-4o-mini)
2. **Qdrant Cloud** - Vector database hosting
3. **Cohere** - Reranking service

### Environment Variables

Create `.env` file in `backend/` directory (see `backend/env.example`):

```bash
# OpenAI API Key (for embeddings and LLM)
OPENAI_API_KEY=sk-...

# Qdrant Cloud Configuration
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=mini_rag_docs

# Cohere API Key (for reranking)
COHERE_API_KEY=...

# Server Configuration (optional)
BACKEND_URL=http://localhost:8000
```

### Frontend Environment
Create `.env.local` in `frontend/`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
# Or your deployed backend URL
```

## 🚀 Deployment

### Backend (Render/Fly.io)

#### Option 1: Render
1. Create new Web Service on Render
2. Connect GitHub repository
3. Set build command: `cd backend && pip install -r requirements.txt`
4. Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard
6. Deploy

#### Option 2: Fly.io
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. In `backend/` directory: `fly launch`
3. Set secrets: `fly secrets set OPENAI_API_KEY=... QDRANT_URL=... QDRANT_API_KEY=... COHERE_API_KEY=...`
4. Deploy: `fly deploy`

### Frontend (Vercel)

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variable: `NEXT_PUBLIC_API_URL` = your backend URL
4. Deploy

### Alternative: Netlify
1. Connect GitHub repository
2. Build command: `cd frontend && npm run build`
3. Publish directory: `frontend/.next`
4. Set environment variable: `NEXT_PUBLIC_API_URL`
5. Deploy

### Live URLs
- **Backend:** [Your Render/Fly.io URL]
- **Frontend:** [Your Vercel/Netlify URL]

## 📦 Installation & Local Development

### Prerequisites
- Python 3.9+
- Node.js 18+
- API keys for OpenAI, Qdrant Cloud, and Cohere

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

### Test
```bash
# In another terminal
python test_ingest.py
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
│   │   ├── embeddings.py       # OpenAI embeddings
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
├── test_ingest.py              # Test script
├── gold_qa_pairs.md            # 5 gold Q/A pairs for evaluation
└── README.md                   # This file
```

## 🧪 Testing

### Manual Testing
1. Start backend: `cd backend && uvicorn main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Upload a document via the UI
4. Query the system
5. Verify citations and sources

### Automated Testing
```bash
python test_ingest.py
```

## 📝 API Endpoints

### POST /ingest
Ingest text or file into the vector database.

**Request:**
- `text` (form): Text content (optional if file provided)
- `file` (file): Uploaded file (optional if text provided)
- `source` (form): Source identifier
- `title` (form): Document title
- `section` (form): Section identifier

**Response:**
```json
{
  "count": 5,
  "collection_name": "mini_rag_docs"
}
```

### POST /query
Query the RAG system.

**Request:**
```json
{
  "q": "What is RAG?"
}
```

**Response:**
```json
{
  "answer": "RAG is... [1] [2]",
  "citations": [
    {"number": 1, "source": "doc1", "section": "intro", "position": 0}
  ],
  "sources": [
    {"source": "doc1", "section": "intro", "position": 0}
  ],
  "latency_ms": 1250.5,
  "token_estimate": 3200,
  "retrieved_ids": [123, 456, 789, 101]
}
```

## 🔒 Security Notes

- **API keys:** Stored server-side only (backend `.env`)
- **CORS:** Configured for frontend domain (update in production)
- **No secrets in frontend:** All API calls go through backend
- **Input validation:** FastAPI validates request formats

## 📄 License

MIT License - feel free to use and modify.

## 🤝 Contributing

This is a minimal implementation following the assessment spec. For production use, consider the "What's Next" improvements above.

---

**Built with:** FastAPI, Next.js, Qdrant Cloud, OpenAI, Cohere
