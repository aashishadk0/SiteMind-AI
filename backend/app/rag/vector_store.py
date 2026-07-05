"""
ChromaDB vector store.
"""

import chromadb

from backend.app.config import CHROMA_DIR


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        self.collection = self.client.get_or_create_collection(
            name="knowledge_base"
        )

    def add_chunks(self, chunks):
        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunks:
            ids.append(str(chunk["chunk_id"]))
            documents.append(chunk["content"])
            embeddings.append(chunk["embedding"])

            metadatas.append({
                "user_id": str(chunk["user_id"]),
                "source_id": str(chunk["source_id"]),
                "source_name": chunk["source_name"],
                "website": chunk["website"],
                "title": chunk["page_title"],
                "url": chunk["url"]
            })

        if documents:
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )

    def search(self, embedding, top_k=5, user_id=None, source_id=None):
        where_filter = None

        if user_id and source_id:
            where_filter = {
                "$and": [
                    {"user_id": str(user_id)},
                    {"source_id": str(source_id)}
                ]
            }

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=where_filter
        )

    def delete_source_vectors(self, user_id, source_id):
        try:
            self.collection.delete(
                where={
                    "$and": [
                        {"user_id": str(user_id)},
                        {"source_id": str(source_id)}
                    ]
                }
            )
        except Exception:
            pass