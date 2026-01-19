"""
Cohere Rerank v3 for reranking retrieved chunks.
"""

import os
from typing import List, Dict, Any
import cohere


class CohereReranker:
    """
    Reranks chunks using Cohere rerank-english-v3.0.
    """

    def __init__(
        self,
        api_key: str = None,
        model: str = "rerank-english-v3.0",
        top_n: int = 4
    ):
        api_key = api_key or os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not set")

        self.client = cohere.Client(api_key)
        self.model = model
        self.top_n = top_n

    def rerank(
        self,
        query: str,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        if not chunks:
            return []

        texts = [c["text"] for c in chunks]

        try:
            response = self.client.rerank(
                model=self.model,
                query=query,
                documents=texts,
                top_n=min(self.top_n, len(texts)),
            )
        except Exception as e:
            # Fail gracefully: return original ranking
            print(f"[WARN] Cohere rerank failed: {e}")
            return chunks[: self.top_n]

        reranked = []
        for r in response.results:
            c = chunks[r.index].copy()
            c["rerank_score"] = r.relevance_score
            reranked.append(c)

        return reranked
