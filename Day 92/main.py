"""
Day 92: Custom Web Scraper to CSV
Phase 5: Portfolio

Key Concepts:
Requests, BeautifulSoup4, CSV Data Normalization, E-Commerce/Job Extraction
"""

import os
import sys
from typing import List

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO, SCRAPER_ICON
from scraper import WebScraperEngine, ScrapedRecord, SAMPLE_HN_HTML, SAMPLE_BOOKS_HTML


def banner():
    """Prints the project banner and ASCII art."""
    print("=" * 72)
    print(LOGO)
    print("=" * 72)
    print(" 🚀 DAY 92: CUSTOM WEB SCRAPER TO CSV")
    print(" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print(" Key Concepts: Requests, BeautifulSoup4, CSV Normalization, Data Pipeline")
    print("=" * 72 + "\n")


def display_records(records: List[ScrapedRecord], limit: int = 10):
    """Prints a formatted tabular view of scraped records."""
    if not records:
        print("  [i] No records to display.")
        return

    print(f"\n  {'#':<4} | {'Title':<42} | {'Author / Brand':<15} | {'Metric':<12} | {'Category'}")
    print("  " + "-" * 95)
    for idx, r in enumerate(records[:limit], 1):
        clean_title = (r.title[:39] + "...") if len(r.title) > 42 else r.title
        metric_str = f"{r.metric_value} {r.metric_label}"
        print(f"  {idx:<4} | {clean_title:<42} | {r.author_or_brand:<15} | {metric_str:<12} | {r.category}")
    
    if len(records) > limit:
        print(f"  ... and {len(records) - limit} more records (total: {len(records)}).")
    print()


def run_automated_tests():
    """Validates the web scraper parsing, normalization, filtering, and CSV pipeline."""
    print("\n🔍 Running Day 92 Automated Web Scraper & CSV Pipeline Test Suite...")
    print("-" * 70)

    engine = WebScraperEngine()

    # 1. Hacker News parsing test
    hn_items = engine.parse_hacker_news(SAMPLE_HN_HTML)
    assert len(hn_items) == 3, f"Expected 3 HN items, got {len(hn_items)}"
    assert "Gemini 1.5 Pro" in hn_items[0].title
    assert hn_items[0].metric_value == 428.0
    assert hn_items[0].author_or_brand == "ai_researcher"
    assert hn_items[0].secondary_metric == 182
    print(" [PASS] 1. Hacker News HTML parsing verified (3 stories, scores, comments, authors).")

    # 2. Books catalog parsing test
    book_items = engine.parse_books_catalog(SAMPLE_BOOKS_HTML)
    assert len(book_items) == 4, f"Expected 4 books, got {len(book_items)}"
    assert book_items[0].title == "A Light in the Attic"
    assert book_items[0].metric_value == 51.77
    assert book_items[0].secondary_metric == 3  # Three stars
    print(" [PASS] 2. Books Catalog HTML parsing verified (4 items, price float conversion, star rating).")

    # 3. Multi-criteria filtering
    filtered_hn = engine.filter_records(hn_items, keyword="python", min_metric=200.0)
    assert len(filtered_hn) == 1
    assert "Python 3.12" in filtered_hn[0].title
    print(" [PASS] 3. Multi-criteria filtering verified (keyword + threshold filtering).")

    # 4. CSV export validation
    test_csv = os.path.join(os.path.dirname(__file__), "test_output.csv")
    combined = hn_items + book_items
    engine.export_to_csv(combined, test_csv)
    assert os.path.exists(test_csv)
    with open(test_csv, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 8  # header + 7 items
        assert "metric_value" in lines[0]
    os.remove(test_csv)
    print(" [PASS] 4. CSV generation and standard headers validated.")

    # 5. Statistical summary
    summary = engine.compute_summary(combined)
    assert summary["count"] == 7
    assert summary["categories"]["Tech News"] == 3
    assert summary["categories"]["Book Catalog"] == 4
    print(" [PASS] 5. Statistical aggregation metrics verified.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Custom Web Scraper to CSV pipeline fully operational.\n")


def interactive_cli():
    """Interactive command-line harvester."""
    banner()
    engine = WebScraperEngine()
    current_dataset: List[ScrapedRecord] = []

    while True:
        print("\n" + "=" * 55)
        print("  WEB SCRAPER & CSV HARVESTER MENU")
        print("=" * 55)
        print("  [1] Scrape Hacker News Headlines (Live or Offline Sample)")
        print("  [2] Scrape Books Catalog (Live or Offline Sample)")
        print("  [3] Filter Current Dataset (Keyword / Min Score)")
        print("  [4] Export Dataset to CSV File")
        print("  [5] View Dataset Summary Analytics")
        print("  [6] Run Automated Test Suite")
        print("  [7] Exit")
        print("=" * 55)

        choice = input("Enter option (1-7): ").strip()

        if choice == "1":
            print("\n  [+] Harvesting Hacker News...")
            records = engine.scrape_hacker_news()
            current_dataset = records
            print(f"  [✓] Successfully scraped {len(records)} stories.")
            display_records(current_dataset)

        elif choice == "2":
            print("\n  [+] Harvesting Books Catalog...")
            records = engine.scrape_books_catalog()
            current_dataset = records
            print(f"  [✓] Successfully scraped {len(records)} products.")
            display_records(current_dataset)

        elif choice == "3":
            if not current_dataset:
                print("  [!] Dataset is empty. Please scrape some data first.")
                continue
            kw = input("  Enter search keyword (or press Enter to skip): ").strip()
            min_val_str = input("  Enter minimum score/price (or press Enter for 0): ").strip()
            min_val = float(min_val_str) if min_val_str else 0.0
            filtered = engine.filter_records(current_dataset, keyword=kw if kw else None, min_metric=min_val)
            print(f"\n  [✓] Filtered {len(filtered)} matching records out of {len(current_dataset)}.")
            display_records(filtered)

        elif choice == "4":
            if not current_dataset:
                print("  [!] Dataset is empty. Please scrape some data first.")
                continue
            filename = input("  Enter CSV filename (default: 'scraped_dataset.csv'): ").strip()
            if not filename:
                filename = "scraped_dataset.csv"
            filepath = os.path.join(os.path.dirname(__file__), filename)
            engine.export_to_csv(current_dataset, filepath)
            print(f"  [✓] Exported {len(current_dataset)} records to: {filepath}")

        elif choice == "5":
            if not current_dataset:
                print("  [!] Dataset is empty. Please scrape some data first.")
                continue
            summary = engine.compute_summary(current_dataset)
            print("\n  📊 Dataset Analytics:")
            print(f"     Total Records : {summary['count']}")
            print(f"     Average Value : {summary['avg_metric']}")
            print(f"     Max Value     : {summary['max_metric']}")
            print(f"     Min Value     : {summary['min_metric']}")
            print(f"     Breakdown     : {summary['categories']}")

        elif choice == "6":
            run_automated_tests()

        elif choice == "7":
            print("\n👋 Exiting Web Scraper Harvester. Happy Coding!\n")
            break
        else:
            print("  [!] Invalid option. Please choose 1-7.")


def main():
    try:
        interactive_cli()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 92 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
