"""
Retrieve relevant chunks from selected user's selected knowledge source.
"""

from backend.app.rag.embeddings import EmbeddingService
from backend.app.rag.vector_store import VectorStore


class Retriever:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def retrieve(self, question: str, top_k: int = 5, user_id=None, source_id=None):
        embedding = self.embedding_service.embed(question)

        results = self.vector_store.search(
            embedding=embedding,
            top_k=top_k,
            user_id=user_id,
            source_id=source_id
        )

        retrieved = []

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for doc, meta, distance in zip(documents, metadatas, distances):
            retrieved.append({
                "content": doc,
                "user_id": meta.get("user_id"),
                "source_id": meta.get("source_id"),
                "source_name": meta.get("source_name"),
                "website": meta.get("website"),
                "title": meta.get("title"),
                "url": meta.get("url"),
                "score": 1 - distance
            })

        return retrieved