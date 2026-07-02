from crawler import WebsiteCrawler

crawler = WebsiteCrawler(
    "https://lict.edu.np",
    max_pages=30
)

pages = crawler.crawl()

print()

print("=" * 60)

print("DISCOVERED PAGES")

print("=" * 60)

for page in pages:

    print(page)

print()

print(f"Total Pages : {len(pages)}")