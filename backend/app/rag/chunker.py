class RecursiveChunker:
    def __init__(self, chunk_size=250, overlap=40):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_pages(self, knowledge: dict, source_id: int):
        chunks = []
        chunk_id = 1

        website = knowledge["website"]["name"]

        for page in knowledge["pages"]:
            page_chunks = self._chunk_page(
                source_id=source_id,
                source_name=website,
                website=website,
                page=page,
                start_id=chunk_id
            )

            chunks.extend(page_chunks)
            chunk_id += len(page_chunks)

        return chunks

    def _chunk_page(self, source_id, source_name, website, page, start_id):
        content = page.get("content", "")
        words = content.split()

        chunks = []
        current = 0
        chunk_id = start_id

        while current < len(words):
            end = current + self.chunk_size
            chunk_words = words[current:end]

            chunks.append({
                "chunk_id": f"{source_id}_{chunk_id}",
                "source_id": source_id,
                "source_name": source_name,
                "website": website,
                "page_title": page.get("title", ""),
                "url": page.get("url", ""),
                "headings": page.get("headings", []),
                "content": " ".join(chunk_words),
                "word_count": len(chunk_words)
            })

            chunk_id += 1
            current += self.chunk_size - self.overlap

        return chunks