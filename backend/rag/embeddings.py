import os
from typing import List
import cohere
from dotenv import load_dotenv


class EmbeddingGenerator:
    """
    Generates embeddings using Cohere embed-english-v3.0 (1024-D).
    """

    def __init__(self, api_key: str = None):
        load_dotenv("environment.env")

        api_key = api_key or os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not set")

        self.client = cohere.Client(api_key)
        self.model = "embed-english-v3.0"
        self.dimension = 1024

    def embed(
        self,
        texts: List[str],
        mode: str = "document"  # "document" or "query"
    ) -> List[List[float]]:
        if not texts:
            return []

        input_type = (
            "search_document"
            if mode == "document"
            else "search_query"
        )

        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type=input_type
        )

        return response.embeddings
