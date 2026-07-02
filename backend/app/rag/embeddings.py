"""
Embedding service using Ollama.
"""

from ollama import Client

from backend.app.config import OLLAMA_URL


class EmbeddingService:
    """Generate embeddings using Ollama."""

    def __init__(self):

        self.client = Client(host=OLLAMA_URL)

        self.model = "nomic-embed-text"

    def embed(self, text: str):

        response = self.client.embed(
            model=self.model,
            input=text
        )

        return response["embeddings"][0]

    def embed_documents(self, texts: list[str]):

        response = self.client.embed(
            model=self.model,
            input=texts
        )

        return response["embeddings"]