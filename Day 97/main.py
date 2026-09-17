"""
Day 97: Automated Scraping & Email Digest Newsletter
Phase 5: Portfolio

Key Concepts:
Web Scraping, HTML Email Templates, smtplib Automation, Scheduled Trigger
"""

import os
import sys
import tempfile

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO, MAIL_SCENE
from digest_engine import NewsletterEngine, SubscriberManager, DigestArticle


def banner():
    """Prints the project banner and ASCII art."""
    print("=" * 72)
    print(LOGO)
    print(MAIL_SCENE)
    print("=" * 72)
    print(" 🚀 DAY 97: AUTOMATED SCRAPING & EMAIL DIGEST NEWSLETTER")
    print(" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print(" Key Concepts: Web Scraping, HTML Templates, MIME Packaging, Dispatch Engine")
    print("=" * 72 + "\n")


def run_automated_tests():
    """Validates article harvesting, email template construction, and MIME dispatch."""
    print("\n🔍 Running Day 97 Automated Newsletter & Email Dispatch Test Suite...")
    print("-" * 70)

    temp_dir = tempfile.mkdtemp()
    temp_subs = os.path.join(temp_dir, "test_subs.json")

    # 1. Subscriber manager CRUD & deduplication
    mgr = SubscriberManager(temp_subs, default_subscribers=[])
    assert mgr.add_subscriber("alice@test.org") is True
    assert mgr.add_subscriber("alice@test.org") is False  # duplicate prevention
    assert mgr.add_subscriber("bob@test.org") is True
    assert len(mgr.get_all()) == 2
    assert mgr.remove_subscriber("alice@test.org") is True
    assert len(mgr.get_all()) == 1
    print(" [PASS] 1. Subscriber persistence, deduplication, and removal verified.")

    # 2. Article harvesting
    engine = NewsletterEngine(subscribers_path=temp_subs)
    articles = engine.fetch_articles(force_offline=True)
    assert len(articles) >= 4
    assert any("Python" in a.title for a in articles)
    print(" [PASS] 2. Digest article harvesting and structured metadata mapping verified.")

    # 3. HTML template compilation
    html = engine.generate_html_email(articles, "recipient@test.org")
    assert "<!DOCTYPE html>" in html
    assert "TechPulse Daily" in html
    assert "recipient@test.org" in html
    assert "Python 3.13" in html
    print(" [PASS] 3. Responsive dark-mode HTML email template rendering verified.")

    # 4. MIME multipart packaging
    mime_msg = engine.build_mime_message(articles, "recipient@test.org")
    assert mime_msg.is_multipart()
    parts = mime_msg.get_payload()
    assert len(parts) == 2
    assert parts[0].get_content_type() == "text/plain"
    assert parts[1].get_content_type() == "text/html"
    print(" [PASS] 4. RFC 2822 dual-payload (Plaintext + HTML) MIME construction verified.")

    # 5. Outbox dispatch dry-run
    res = engine.dispatch_digest(dry_run=True)
    assert res["subscribers_count"] == 1
    assert len(res["dispatches"]) == 1
    saved_file = res["dispatches"][0]["file"]
    assert os.path.exists(saved_file)
    with open(saved_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "newsletter@pythonbootcamp.internal" in content
        assert "bob@test.org" in content
    print(" [PASS] 5. Automated sandbox file dispatch & message serialization verified.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Automated Newsletter & Digest Pipeline fully operational.\n")


def interactive_cli():
    """Interactive command-line interface."""
    banner()
    engine = NewsletterEngine()

    while True:
        print("\n" + "=" * 55)
        print("  TECHPULSE NEWSLETTER COMMAND CENTER")
        print("=" * 55)
        print("  [1] Preview Today's Curated Articles Feed")
        print("  [2] View & Manage Subscriber List")
        print("  [3] Add New Subscriber Email")
        print("  [4] Dispatch Daily Digest (Sandbox / Outbox)")
        print("  [5] Run Automated Test Suite")
        print("  [6] Exit")
        print("=" * 55)

        choice = input("Enter option (1-6): ").strip()

        if choice == "1":
            articles = engine.fetch_articles()
            print("\n  📰 TODAY'S CURATED STORIES:")
            print("  " + "-" * 70)
            for idx, a in enumerate(articles, 1):
                print(f"  [{idx}] [{a.badge}] {a.title}")
                print(f"      Source : {a.source} | URL: {a.url}")
                print(f"      Summary: {a.summary}\n")

        elif choice == "2":
            subs = engine.sub_mgr.get_all()
            print("\n  📬 ACTIVE NEWSLETTER SUBSCRIBERS:")
            print("  " + "-" * 50)
            for s in subs:
                print(f"  • {s}")
            print(f"  Total subscribers: {len(subs)}")

        elif choice == "3":
            new_email = input("  Enter email to subscribe: ").strip()
            if engine.sub_mgr.add_subscriber(new_email):
                print(f"  [✓] Successfully subscribed {new_email} to TechPulse Daily!")
            else:
                print("  [!] Invalid email or already subscribed.")

        elif choice == "4":
            print("\n  🚀 Executing automated newsletter dispatch...")
            res = engine.dispatch_digest(dry_run=True)
            print(f"  [✓] Dispatched to {res['subscribers_count']} subscribers!")
            for d in res["dispatches"]:
                print(f"      -> {d['recipient']}: {d['file']}")
            print("  Check Day 97/outbox/ to view generated .eml files!")

        elif choice == "5":
            run_automated_tests()

        elif choice == "6":
            print("\n👋 Exiting TechPulse Newsletter. Happy Coding!\n")
            break
        else:
            print("  [!] Invalid option. Please choose 1-6.")


def main():
    try:
        interactive_cli()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 97 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
