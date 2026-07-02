"""
Knowledge Base Builder.

Converts scraped pages into a structured JSON file.
"""

import json
from datetime import datetime
from pathlib import Path


class JSONBuilder:
    """Build and save structured website knowledge."""

    def __init__(self, output_dir: Path):

        self.output_dir = output_dir

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def build(
        self,
        website_name: str,
        source_url: str,
        pages: list
    ) -> dict:
        """
        Build the final knowledge structure.
        """

        return {
            "website": {
                "name": website_name,
                "source": source_url,
                "created_at": datetime.utcnow().isoformat(),
                "total_pages": len(pages),
            },
            "pages": pages
        }

    def save(
        self,
        knowledge: dict,
        filename: str
    ) -> Path:
        """
        Save knowledge base as JSON.
        """

        file_path = self.output_dir / filename

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                knowledge,
                file,
                indent=4,
                ensure_ascii=False
            )

        return file_path