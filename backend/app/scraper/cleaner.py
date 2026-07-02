"""
HTML cleaning utilities.

Responsible for extracting meaningful content from HTML.
"""

import re

from bs4 import BeautifulSoup


class HTMLCleaner:
    """Extract clean readable text from HTML."""

    def clean(self, html: str) -> dict:
        """
        Convert raw HTML into structured content.
        """

        soup = BeautifulSoup(html, "html.parser")

        # Remove unwanted elements
        self._remove_unwanted_tags(soup)

        title = self._extract_title(soup)

        headings = self._extract_headings(soup)

        text = self._extract_text(soup)

        return {
            "title": title,
            "headings": headings,
            "content": text
        }

    def _remove_unwanted_tags(self, soup):

        unwanted = [
            "script",
            "style",
            "noscript",
            "svg",
            "canvas",
            "iframe",
            "footer",
            "nav",
            "aside",
            "form",
        ]

        for tag in unwanted:

            for element in soup.find_all(tag):

                element.decompose()

    def _extract_title(self, soup):

        if soup.title:

            return soup.title.get_text(
                " ",
                strip=True
            )

        return ""

    def _extract_headings(self, soup):

        headings = []

        for tag in soup.find_all(
            ["h1", "h2", "h3"]
        ):

            text = tag.get_text(
                " ",
                strip=True
            )

            if text:

                headings.append(text)

        return headings

    def _extract_text(self, soup):

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()