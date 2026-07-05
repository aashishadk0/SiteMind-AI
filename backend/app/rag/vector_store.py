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

    def search(self, embedding, top_k=5, source_id=None):
        where_filter = None

        if source_id:
            where_filter = {
                "source_id": str(source_id)
            }

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=where_filter
        )