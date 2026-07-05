"""
Knowledge indexing service.
"""

from backend.app.config import STRUCTURED_DATA_DIR
from backend.app.database.knowledge_repository import KnowledgeRepository
from backend.app.scraper.crawler import WebsiteCrawler
from backend.app.scraper.scraper import WebsiteScraper
from backend.app.scraper.json_builder import JSONBuilder
from backend.app.rag.chunker import RecursiveChunker
from backend.app.rag.embeddings import EmbeddingService
from backend.app.rag.vector_store import VectorStore


class KnowledgeService:
    def __init__(self):
        self.repo = KnowledgeRepository()
        self.scraper = WebsiteScraper()
        self.builder = JSONBuilder(STRUCTURED_DATA_DIR)
        self.chunker = RecursiveChunker()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def index_website(self, user_id, name, url, max_pages=20):
        source_id = self.repo.create_source(
            user_id=user_id,
            name=name,
            base_url=url
        )

        try:
            self.repo.update_progress(
                source_id,
                "crawling",
                "Crawling website pages..."
            )

            crawler = WebsiteCrawler(
                url,
                max_pages=max_pages
            )

            urls = crawler.crawl()

            self.repo.update_progress(
                source_id,
                "cleaning",
                f"Found {len(urls)} pages. Cleaning content..."
            )

            pages = []

            for page_url in urls:
                try:
                    page = self.scraper.scrape(page_url)
                    pages.append(page)
                except Exception:
                    continue

            self.repo.update_progress(
                source_id,
                "structuring",
                "Creating structured knowledge base..."
            )

            knowledge = self.builder.build(
                website_name=name,
                source_url=url,
                pages=pages
            )

            safe_name = name.lower().replace(" ", "_")

            self.builder.save(
                knowledge,
                f"user_{user_id}_{safe_name}_{source_id}.json"
            )

            self.repo.update_progress(
                source_id,
                "chunking",
                "Splitting content into searchable chunks..."
            )

            chunks = self.chunker.chunk_pages(
                knowledge=knowledge,
                user_id=user_id,
                source_id=source_id
            )

            self.repo.update_progress(
                source_id,
                "embedding",
                "Creating embeddings and storing vectors..."
            )

            for chunk in chunks:
                chunk["embedding"] = self.embedding_service.embed(
                    chunk["content"]
                )

            self.vector_store.add_chunks(chunks)

            self.repo.update_progress(
                source_id,
                "ready",
                "Indexing completed successfully.",
                total_pages=len(pages)
            )

            return {
                "source_id": source_id,
                "name": name,
                "url": url,
                "total_pages": len(pages),
                "status": "ready"
            }

        except Exception as error:
            self.repo.update_progress(
                source_id,
                "failed",
                f"Indexing failed: {str(error)}"
            )

            raise error

    def list_sources(self, user_id):
        return self.repo.list_sources(user_id)

    def get_source(self, source_id, user_id):
        return self.repo.get_source(source_id, user_id)

    def delete_source(self, source_id, user_id):
        self.vector_store.delete_source_vectors(user_id, source_id)
        self.repo.delete_source(source_id, user_id)

        return {
            "message": "Knowledge source deleted."
        }