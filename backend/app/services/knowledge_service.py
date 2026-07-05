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

    def index_website(self, name, url, max_pages=20):
        source = self.repo.create_source(
            name=name,
            base_url=url,
            status="indexing"
        )

        source_id = source["id"]

        try:
            crawler = WebsiteCrawler(
                url,
                max_pages=max_pages
            )

            urls = crawler.crawl()

            pages = []

            for page_url in urls:
                try:
                    page = self.scraper.scrape(page_url)
                    pages.append(page)
                except Exception:
                    continue

            knowledge = self.builder.build(
                website_name=name,
                source_url=url,
                pages=pages
            )

            safe_name = name.lower().replace(" ", "_")

            self.builder.save(
                knowledge,
                f"{safe_name}_{source_id}.json"
            )

            chunks = self.chunker.chunk_pages(
                knowledge,
                source_id=source_id
            )

            for chunk in chunks:
                chunk["embedding"] = self.embedding_service.embed(
                    chunk["content"]
                )

            self.vector_store.add_chunks(chunks)

            self.repo.update_source(
                source_id=source_id,
                status="ready",
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
            self.repo.update_source(
                source_id=source_id,
                status="failed",
                total_pages=0
            )

            raise error

    def list_sources(self):
        return self.repo.list_sources()

    def delete_source(self, source_id):
        self.repo.delete_source(source_id)

        return {
            "message": "Knowledge source deleted."
        }