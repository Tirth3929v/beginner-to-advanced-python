"""
Day 92: Custom Web Scraper to CSV
Extraction, Data Normalization, and CSV Export Engine
"""

import csv
import os
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
import requests

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)

# Deterministic offline sample HTML for testing and offline resilience
SAMPLE_HN_HTML = """
<!DOCTYPE html>
<html>
<head><title>Hacker News</title></head>
<body>
<table id="hnmain">
  <tr class="athing" id="38000001">
    <td align="right" valign="top" class="title"><span class="rank">1.</span></td>
    <td valign="top" class="votelinks"><center><a id="up_38000001" href="vote?id=38000001">^</a></center></td >
    <td class="title"><span class="titleline"><a href="https://deepmind.google/technologies/gemini/">Gemini 1.5 Pro Technical Report and Scalable Reasoning</a><span class="sitebit comhead"> (<a href="from?site=deepmind.google"><span class="sitestr">deepmind.google</span></a>)</span></span></td>
  </tr>
  <tr>
    <td colspan="2"></td>
    <td class="subtext">
      <span class="subline">
        <span class="score" id="score_38000001">428 points</span> by <a href="user?id=ai_researcher" class="hnuser">ai_researcher</a> <span class="age"><a href="item?id=38000001">3 hours ago</a></span> | <a href="item?id=38000001">182 comments</a>
      </span>
    </td>
  </tr>
  <tr class="spacer" style="height:5px"></tr>
  <tr class="athing" id="38000002">
    <td align="right" valign="top" class="title"><span class="rank">2.</span></td>
    <td valign="top" class="votelinks"><center><a id="up_38000002" href="vote?id=38000002">^</a></center></td >
    <td class="title"><span class="titleline"><a href="https://python.org/release-3-12/">Python 3.12: Faster CPython, Per-Interpreter GIL, Better Errors</a><span class="sitebit comhead"> (<a href="from?site=python.org"><span class="sitestr">python.org</span></a>)</span></span></td>
  </tr>
  <tr>
    <td colspan="2"></td>
    <td class="subtext">
      <span class="subline">
        <span class="score" id="score_38000002">285 points</span> by <a href="user?id=guido_fan" class="hnuser">guido_fan</a> <span class="age"><a href="item?id=38000002">5 hours ago</a></span> | <a href="item?id=38000002">94 comments</a>
      </span>
    </td>
  </tr>
  <tr class="spacer" style="height:5px"></tr>
  <tr class="athing" id="38000003">
    <td align="right" valign="top" class="title"><span class="rank">3.</span></td>
    <td valign="top" class="votelinks"><center><a id="up_38000003" href="vote?id=38000003">^</a></center></td >
    <td class="title"><span class="titleline"><a href="https://rust-lang.org/edition-2024/">Rust 2024 Edition Preview & Async Foundations</a><span class="sitebit comhead"> (<a href="from?site=rust-lang.org"><span class="sitestr">rust-lang.org</span></a>)</span></span></td>
  </tr>
  <tr>
    <td colspan="2"></td>
    <td class="subtext">
      <span class="subline">
        <span class="score" id="score_38000003">173 points</span> by <a href="user?id=ferris_crab" class="hnuser">ferris_crab</a> <span class="age"><a href="item?id=38000003">7 hours ago</a></span> | <a href="item?id=38000003">56 comments</a>
      </span>
    </td>
  </tr>
</table>
</body>
</html>
"""

SAMPLE_BOOKS_HTML = """
<!DOCTYPE html>
<html>
<body>
<div class="row">
  <article class="product_pod">
    <div class="image_container"><a href="catalogue/a-light-in-the-attic_1000/index.html"><img src="media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg" alt="A Light in the Attic" class="thumbnail"></a></div>
    <p class="star-rating Three"><i class="icon-star"></i></p>
    <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the Attic</a></h3>
    <div class="product_price">
      <p class="price_color">£51.77</p>
      <p class="instock availability"><i class="icon-ok"></i> In stock</p>
    </div>
  </article>
  <article class="product_pod">
    <div class="image_container"><a href="catalogue/tipping-the-velvet_999/index.html"><img src="media/cache/26/0e/260e9881cceb699c00eb9d96ff2735f0.jpg" alt="Tipping the Velvet" class="thumbnail"></a></div>
    <p class="star-rating One"><i class="icon-star"></i></p>
    <h3><a href="catalogue/tipping-the-velvet_999/index.html" title="Tipping the Velvet">Tipping the Velvet</a></h3>
    <div class="product_price">
      <p class="price_color">£53.74</p>
      <p class="instock availability"><i class="icon-ok"></i> In stock</p>
    </div>
  </article>
  <article class="product_pod">
    <div class="image_container"><a href="catalogue/soumission_998/index.html"><img src="media/cache/3e/ef/3eef99c9d9e431b4e69e013ca05d32ac.jpg" alt="Soumission" class="thumbnail"></a></div>
    <p class="star-rating One"><i class="icon-star"></i></p>
    <h3><a href="catalogue/soumission_998/index.html" title="Soumission">Soumission</a></h3>
    <div class="product_price">
      <p class="price_color">£50.10</p>
      <p class="instock availability"><i class="icon-ok"></i> In stock</p>
    </div>
  </article>
  <article class="product_pod">
    <div class="image_container"><a href="catalogue/sharp-objects_997/index.html"><img src="media/cache/32/e1/32e1047d81db9e65476497d9b7b7d089.jpg" alt="Sharp Objects" class="thumbnail"></a></div>
    <p class="star-rating Four"><i class="icon-star"></i></p>
    <h3><a href="catalogue/sharp-objects_997/index.html" title="Sharp Objects">Sharp Objects</a></h3>
    <div class="product_price">
      <p class="price_color">£47.82</p>
      <p class="instock availability"><i class="icon-ok"></i> In stock</p>
    </div>
  </article>
</div>
</body>
</html>
"""

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


@dataclass
class ScrapedRecord:
    id: str
    title: str
    link: str
    author_or_brand: str
    metric_value: float  # e.g., points or price in GBP/USD
    metric_label: str    # "points" or "price_gbp"
    secondary_metric: int # comments or star rating
    secondary_label: str  # "comments" or "stars"
    category: str        # "Tech News" or "Book Catalog"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class WebScraperEngine:
    def __init__(self, user_agent: str = DEFAULT_USER_AGENT):
        self.headers = {"User-Agent": user_agent}

    def fetch_url(self, url: str, timeout: int = 5) -> Optional[str]:
        """Fetches page content with timeout and error handling."""
        try:
            resp = requests.get(url, headers=self.headers, timeout=timeout)
            if resp.status_code == 200:
                return resp.text
            return None
        except Exception:
            return None

    def parse_hacker_news(self, html_content: str) -> List[ScrapedRecord]:
        """Parses Hacker News HTML into structured ScrapedRecords."""
        soup = BeautifulSoup(html_content, "html.parser")
        records = []
        athing_rows = soup.find_all("tr", class_="athing")

        for row in athing_rows:
            item_id = row.get("id", "0")
            title_tag = row.find("span", class_="titleline")
            if not title_tag:
                continue
            
            link_tag = title_tag.find("a")
            title = link_tag.get_text(strip=True) if link_tag else "No Title"
            link = link_tag.get("href", "") if link_tag else ""

            # Next sibling row contains the subtext (score, author, comments)
            subtext_row = row.find_next_sibling("tr")
            score = 0
            author = "Unknown"
            comments = 0

            if subtext_row:
                subtext = subtext_row.find("td", class_="subtext")
                if subtext:
                    score_tag = subtext.find("span", class_="score")
                    if score_tag:
                        score_match = re.search(r"(\d+)", score_tag.get_text())
                        if score_match:
                            score = int(score_match.group(1))

                    author_tag = subtext.find("a", class_="hnuser")
                    if author_tag:
                        author = author_tag.get_text(strip=True)

                    links = subtext.find_all("a")
                    for a in links:
                        text = a.get_text()
                        if "comment" in text:
                            comm_match = re.search(r"(\d+)", text)
                            if comm_match:
                                comments = int(comm_match.group(1))

            records.append(
                ScrapedRecord(
                    id=item_id,
                    title=title,
                    link=link,
                    author_or_brand=author,
                    metric_value=float(score),
                    metric_label="points",
                    secondary_metric=comments,
                    secondary_label="comments",
                    category="Tech News"
                )
            )

        return records

    def parse_books_catalog(self, html_content: str) -> List[ScrapedRecord]:
        """Parses Books to Scrape catalog HTML into structured ScrapedRecords."""
        soup = BeautifulSoup(html_content, "html.parser")
        records = []
        articles = soup.find_all("article", class_="product_pod")

        for idx, article in enumerate(articles, 1):
            h3 = article.find("h3")
            title = h3.find("a").get("title", h3.get_text(strip=True)) if h3 else f"Book #{idx}"
            link = h3.find("a").get("href", "") if (h3 and h3.find("a")) else ""

            # Rating
            rating_p = article.find("p", class_=lambda c: c and "star-rating" in c)
            stars = 0
            if rating_p:
                classes = rating_p.get("class", [])
                for cls in classes:
                    if cls in RATING_MAP:
                        stars = RATING_MAP[cls]
                        break

            # Price
            price_p = article.find("p", class_="price_color")
            price = 0.0
            if price_p:
                price_match = re.search(r"[\d\.]+", price_p.get_text())
                if price_match:
                    price = float(price_match.group(0))

            records.append(
                ScrapedRecord(
                    id=f"book_{idx}",
                    title=title,
                    link=link,
                    author_or_brand="BooksToScrape",
                    metric_value=price,
                    metric_label="price_gbp",
                    secondary_metric=stars,
                    secondary_label="stars",
                    category="Book Catalog"
                )
            )

        return records

    def scrape_hacker_news(self, force_offline: bool = False) -> List[ScrapedRecord]:
        """Scrapes live Hacker News, gracefully falling back to offline fixture."""
        if not force_offline:
            html = self.fetch_url("https://news.ycombinator.com/")
            if html:
                parsed = self.parse_hacker_news(html)
                if parsed:
                    return parsed
        return self.parse_hacker_news(SAMPLE_HN_HTML)

    def scrape_books_catalog(self, force_offline: bool = False) -> List[ScrapedRecord]:
        """Scrapes live BooksToScrape, gracefully falling back to offline fixture."""
        if not force_offline:
            html = self.fetch_url("https://books.toscrape.com/")
            if html:
                parsed = self.parse_books_catalog(html)
                if parsed:
                    return parsed
        return self.parse_books_catalog(SAMPLE_BOOKS_HTML)

    @staticmethod
    def filter_records(
        records: List[ScrapedRecord],
        keyword: Optional[str] = None,
        min_metric: float = 0.0,
        min_secondary: int = 0
    ) -> List[ScrapedRecord]:
        """Applies multi-criteria filtering to scraped dataset."""
        results = []
        kw = keyword.lower() if keyword else None
        for r in records:
            if kw and kw not in r.title.lower() and kw not in r.author_or_brand.lower():
                continue
            if r.metric_value < min_metric:
                continue
            if r.secondary_metric < min_secondary:
                continue
            results.append(r)
        return results

    @staticmethod
    def export_to_csv(records: List[ScrapedRecord], filepath: str) -> str:
        """Exports scraped records to a clean, standardized CSV file."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        fieldnames = [
            "id",
            "title",
            "link",
            "author_or_brand",
            "metric_value",
            "metric_label",
            "secondary_metric",
            "secondary_label",
            "category"
        ]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for rec in records:
                writer.writerow(rec.to_dict())

        return filepath

    @staticmethod
    def compute_summary(records: List[ScrapedRecord]) -> Dict[str, Any]:
        """Computes summary statistics on scraped data."""
        if not records:
            return {"count": 0, "avg_metric": 0.0, "max_metric": 0.0, "categories": {}}

        values = [r.metric_value for r in records]
        cats: Dict[str, int] = {}
        for r in records:
            cats[r.category] = cats.get(r.category, 0) + 1

        return {
            "count": len(records),
            "avg_metric": round(sum(values) / len(values), 2),
            "max_metric": max(values),
            "min_metric": min(values),
            "categories": cats
        }
