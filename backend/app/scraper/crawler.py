"""
Generic website crawler using Breadth First Search (BFS).

Responsible only for discovering internal pages.
"""

from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class WebsiteCrawler:
    """Generic BFS website crawler."""

    def __init__(self, base_url: str, max_pages: int = 100):

        self.base_url = base_url.rstrip("/")

        self.domain = urlparse(self.base_url).netloc

        self.max_pages = max_pages

        self.visited = set()

        self.discovered = []


    def _is_internal(self, url: str) -> bool:
        """Check whether URL belongs to same domain."""

        parsed = urlparse(url)

        return parsed.netloc in ("", self.domain)


    def _normalize(self, link: str) -> str:
        """Convert relative URL into absolute URL."""

        return urljoin(self.base_url, link).rstrip("/")


    def _valid(self, url: str) -> bool:
        """Ignore unsupported URLs."""

        ignore = (
            "#",
            "mailto:",
            "tel:",
            ".pdf",
            ".jpg",
            ".jpeg",
            ".png",
            ".svg",
            ".gif",
            ".zip",
        )

        return not any(item in url for item in ignore)


    def crawl(self):
        """Start crawling website."""

        queue = deque([self.base_url])

        while queue and len(self.visited) < self.max_pages:

            current = queue.popleft()

            if current in self.visited:
                continue

            self.visited.add(current)

            try:

                response = requests.get(
                    current,
                    timeout=15,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 SiteMindAI/1.0"
                        )
                    },
                )

                response.raise_for_status()

            except Exception:

                continue

            self.discovered.append(current)

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            for tag in soup.find_all("a", href=True):

                url = self._normalize(
                    tag["href"]
                )

                if not self._is_internal(url):
                    continue

                if not self._valid(url):
                    continue

                if url in self.visited:
                    continue

                queue.append(url)

        return self.discovered