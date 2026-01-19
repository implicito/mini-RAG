# Deployment Guide

Quick deployment steps for Mini RAG application.

## Backend Deployment

### Render.com

1. **Create Account:** Sign up at [render.com](https://render.com)

2. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository and branch

3. **Configure:**
   - **Name:** `mini-rag-backend`
   - **Environment:** Python 3
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables:**
   - `OPENAI_API_KEY` = your OpenAI API key
   - `QDRANT_URL` = your Qdrant Cloud URL
   - `QDRANT_API_KEY` = your Qdrant API key
   - `QDRANT_COLLECTION_NAME` = `mini_rag_docs`
   - `COHERE_API_KEY` = your Cohere API key

5. **Deploy:** Click "Create Web Service"

6. **Get URL:** Copy the service URL (e.g., `https://mini-rag-backend.onrender.com`)

### Fly.io

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Initialize:**
   ```bash
   cd backend
   fly launch
   ```

4. **Set Secrets:**
   ```bash
   fly secrets set OPENAI_API_KEY=sk-...
   fly secrets set QDRANT_URL=https://...
   fly secrets set QDRANT_API_KEY=...
   fly secrets set COHERE_API_KEY=...
   ```

5. **Deploy:**
   ```bash
   fly deploy
   ```

## Frontend Deployment

### Vercel

1. **Create Account:** Sign up at [vercel.com](https://vercel.com)

2. **Import Project:**
   - Click "Add New" → "Project"
   - Import your GitHub repository

3. **Configure:**
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `.next` (default)

4. **Environment Variables:**
   - `NEXT_PUBLIC_API_URL` = your backend URL (e.g., `https://mini-rag-backend.onrender.com`)

5. **Deploy:** Click "Deploy"

6. **Get URL:** Copy the deployment URL (e.g., `https://mini-rag.vercel.app`)

### Netlify

1. **Create Account:** Sign up at [netlify.com](https://netlify.com)

2. **New Site from Git:**
   - Connect GitHub repository
   - Select repository

3. **Build Settings:**
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/.next`

4. **Environment Variables:**
   - `NEXT_PUBLIC_API_URL` = your backend URL

5. **Deploy:** Click "Deploy site"

## Post-Deployment

1. **Test Backend:**
   ```bash
   curl https://your-backend-url.com/
   # Should return: {"status":"ok","message":"Mini RAG API"}
   ```

2. **Test Frontend:**
   - Visit your frontend URL
   - Should load without console errors
   - Try uploading a document
   - Try querying

3. **Update CORS (if needed):**
   - In `backend/main.py`, update `allow_origins` to include your frontend URL:
   ```python
   allow_origins=["https://your-frontend.vercel.app"]
   ```

## Troubleshooting

### Backend Issues
- **Port binding:** Make sure to use `$PORT` environment variable (Render) or `0.0.0.0` (Fly.io)
- **API keys:** Verify all environment variables are set correctly
- **Dependencies:** Check that `requirements.txt` includes all packages

### Frontend Issues
- **API connection:** Verify `NEXT_PUBLIC_API_URL` is set correctly
- **CORS errors:** Update backend CORS settings to allow your frontend domain
- **Build errors:** Check Node.js version (18+ required)

## Free Tier Limits

- **Render:** 750 hours/month free, sleeps after 15 min inactivity
- **Fly.io:** 3 shared VMs free, 160GB outbound data
- **Vercel:** Unlimited deployments, 100GB bandwidth
- **Netlify:** 100GB bandwidth, 300 build minutes/month
