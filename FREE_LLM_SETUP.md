# Free LLM Provider Setup Guide

Since OpenAI requires paid credits, here are **completely free alternatives** you can use:

## 🚀 Quick Start: Groq (Recommended - Fastest & Easiest)

**Groq** offers a free tier with very fast inference. It's the easiest to set up.

### Steps:
1. **Get free API key:**
   - Go to https://console.groq.com/
   - Sign up (free)
   - Create an API key
   - Copy the key

2. **Set environment variable:**
   ```bash
   # In backend/.env or set in your environment
   LLM_PROVIDER=groq
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Restart your backend:**
   ```bash
   uvicorn main:app --reload
   ```

That's it! Groq is now your LLM provider. It's fast, free, and works great for RAG.

---

## Alternative Free Options

### Option 2: Google Gemini (Free Tier)

1. **Get API key:**
   - Go to https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Create API key (free)

2. **Set environment:**
   ```bash
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Option 3: Hugging Face (Free Tier)

1. **Get API key:**
   - Go to https://huggingface.co/settings/tokens
   - Sign up (free)
   - Create access token

2. **Set environment:**
   ```bash
   LLM_PROVIDER=huggingface
   HUGGINGFACE_API_KEY=your_hf_token_here
   ```

---

## Comparison

| Provider | Speed | Quality | Free Tier Limit | Setup Difficulty |
|----------|-------|---------|-----------------|------------------|
| **Groq** | ⚡⚡⚡ Very Fast | ⭐⭐⭐⭐ Good | 30 requests/min | ⭐ Easy |
| **Gemini** | ⚡⚡ Fast | ⭐⭐⭐⭐⭐ Excellent | 60 requests/min | ⭐ Easy |
| **Hugging Face** | ⚡ Moderate | ⭐⭐⭐ Good | 30 requests/min | ⭐ Easy |
| **OpenAI** | ⚡⚡ Fast | ⭐⭐⭐⭐⭐ Excellent | ❌ Paid only | ⭐ Easy |

**Recommendation:** Start with **Groq** - it's the fastest and easiest to set up.

---

## Embeddings (Still Free Options)

For embeddings, you have these free options:

### Option 1: Use Hugging Face Embeddings (Local - Completely Free)

Update `backend/rag/embeddings.py` to use local embeddings:

```python
from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    def __init__(self):
        # Free, runs locally, no API needed
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.dimension = 384  # Note: Different from OpenAI's 3072
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()
```

**Note:** This changes dimension from 3072 to 384. You'll need to:
- Update Qdrant collection dimension to 384, OR
- Create a new collection with dimension 384

### Option 2: Keep OpenAI Embeddings (If you have any credits left)

If you have any OpenAI credits, embeddings are much cheaper than LLM calls. You can:
- Use OpenAI for embeddings (cheap)
- Use Groq/Gemini for LLM (free)

### Option 3: Use Cohere Embeddings (If you have Cohere credits)

Since you're already using Cohere for reranking, check if they offer free embedding credits.

---

## Installation

After choosing your provider, install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

The requirements.txt now includes:
- `groq` - For Groq API
- `google-generativeai` - For Gemini
- `huggingface-hub` - For Hugging Face
- `requests` - For API calls

---

## Testing

1. **Set your provider:**
   ```bash
   export LLM_PROVIDER=groq
   export GROQ_API_KEY=your_key_here
   ```

2. **Start backend:**
   ```bash
   uvicorn main:app --reload
   ```

3. **Test query:**
   ```bash
   curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{"q": "What is RAG?"}'
   ```

---

## Troubleshooting

### "API key required" error
- Make sure you set the correct environment variable for your provider
- Check that the API key is correct (no extra spaces)

### "Rate limit exceeded"
- Free tiers have rate limits (usually 30-60 requests/min)
- Wait a moment and try again
- Consider switching to a different provider

### "Connection failed"
- Check your internet connection
- Some providers may be temporarily unavailable
- Try a different provider

---

## Cost Comparison

- **Groq:** $0 (free tier)
- **Gemini:** $0 (free tier)  
- **Hugging Face:** $0 (free tier)
- **OpenAI:** ~$0.15 per 1M tokens (paid)

**For a Mini RAG app, free tiers are more than enough!**
