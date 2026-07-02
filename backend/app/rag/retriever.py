"""
Retrieve relevant chunks from ChromaDB.
"""

from backend.app.rag.embeddings import EmbeddingService
from backend.app.rag.vector_store import VectorStore


class Retriever:
    """Retrieve the most relevant chunks."""

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.vector_store = VectorStore()

    def retrieve(
        self,
        question: str,
        top_k: int = 5
    ):

        embedding = self.embedding_service.embed(question)

        results = self.vector_store.search(
            embedding=embedding,
            top_k=top_k
        )

        retrieved = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, distance in zip(
            documents,
            metadatas,
            distances
        ):

            retrieved.append({

                "content": doc,

                "website": meta["website"],

                "title": meta["title"],

                "url": meta["url"],

                "score": 1 - distance

            })

        return retrieved