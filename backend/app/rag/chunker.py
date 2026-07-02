"""
Recursive chunking for RAG.
"""

import re


class RecursiveChunker:
    """Split structured pages into overlapping chunks."""

    def __init__(
        self,
        chunk_size: int = 250,
        overlap: int = 40
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_pages(self, knowledge: dict):

        chunks = []

        chunk_id = 1

        website = knowledge["website"]["name"]

        for page in knowledge["pages"]:

            page_chunks = self._chunk_page(
                website,
                page,
                chunk_id
            )

            chunks.extend(page_chunks)

            chunk_id += len(page_chunks)

        return chunks

    def _chunk_page(
        self,
        website,
        page,
        start_id
    ):

        content = page["content"]

        words = content.split()

        chunks = []

        current = 0

        chunk_id = start_id

        while current < len(words):

            end = current + self.chunk_size

            chunk_words = words[current:end]

            chunks.append({

                "chunk_id": chunk_id,

                "website": website,

                "page_title": page["title"],

                "url": page["url"],

                "headings": page["headings"],

                "content": " ".join(chunk_words),

                "word_count": len(chunk_words)

            })

            chunk_id += 1

            current += self.chunk_size - self.overlap

        return chunks