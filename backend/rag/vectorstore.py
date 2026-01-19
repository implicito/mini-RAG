import os
import uuid
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class QdrantVectorStore:
    def __init__(
        self,
        url: str = None,
        api_key: str = None,
        collection_name: str = None,
        recreate: bool = False,
    ):
        url = url or os.getenv("QDRANT_URL")
        api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.collection_name = collection_name or "mini_rag_docs"

        self.dimension = 1024  # Cohere embeddings
        self.client = QdrantClient(url=url, api_key=api_key)

        if recreate:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.dimension,
                    distance=Distance.COSINE,
                ),
            )
            try:
                self.client.get_collection(self.collection_name)
            except Exception:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.dimension,
                        distance=Distance.COSINE,
                    ),
                )


    def upsert_chunks(
        self,
        chunks: List[Dict[str, Any]],
        embeddings: List[List[float]],
    ) -> int:
        points = []
        for chunk, emb in zip(chunks, embeddings):
            pid = uuid.uuid5(
                uuid.NAMESPACE_DNS,
                f"{chunk['source']}::{chunk['position']}",
            ).int >> 64

            points.append(
                PointStruct(
                    id=pid,
                    vector=emb,
                    payload={
                        "text": chunk["text"],
                        "source": chunk.get("source"),         
                        "position": chunk.get("position"),
                    },
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )
        return len(points)

    def search(
        self,
        query_embedding: List[float],
        limit: int = 8,
    ) -> List[Dict[str, Any]]:
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
        )

        return [
            {
                "id": r.id,
                "score": r.score,
                **r.payload,
            }
            for r in results
        ]
