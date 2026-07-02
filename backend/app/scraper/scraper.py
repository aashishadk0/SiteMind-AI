"""
Website scraper.

Downloads HTML and converts it into clean structured data.
"""

import requests

from .cleaner import HTMLCleaner


class WebsiteScraper:

    def __init__(self):

        self.cleaner = HTMLCleaner()

    def scrape(self, url: str):

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0 SiteMindAI/1.0"
            },
        )

        response.raise_for_status()

        html = response.text

        data = self.cleaner.clean(html)

        data["url"] = url

        return data