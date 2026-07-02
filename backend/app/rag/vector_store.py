"""
Vector database using ChromaDB.
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

                "website": chunk["website"],

                "title": chunk["page_title"],

                "url": chunk["url"]

            })

        self.collection.add(

            ids=ids,

            documents=documents,

            embeddings=embeddings,

            metadatas=metadatas

        )

    def search(
        self,
        embedding,
        top_k=5
    ):

        return self.collection.query(

            query_embeddings=[embedding],

            n_results=top_k

        )