from typing import List, Dict, Any
from rag.vectorstore import QdrantVectorStore
from rag.embeddings import EmbeddingGenerator


class MMRRetriever:
    def __init__(
        self,
        vectorstore: QdrantVectorStore,
        embedding_generator: EmbeddingGenerator,
        k: int = 8,
    ):
        self.vectorstore = vectorstore
        self.embedding_generator = embedding_generator
        self.k = k

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        query_embedding = self.embedding_generator.embed(
            [query],
            mode="query"
        )[0]

        return self.vectorstore.search(
            query_embedding=query_embedding,
            limit=self.k,
        )
