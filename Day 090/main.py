"""
Day 90: Convert PDF to Audiobook
Interactive PDF Text Extraction & Speech Synthesis CLI
"""

import sys
import os

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO
from audiobook_converter import AudiobookConverter


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 90: CONVERT PDF TO AUDIOBOOK (TEXT-TO-SPEECH SYNTHESIZER)")
    print(" 📚 Phase 4: Professional Portfolio Projects | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Speech Engineering Highlights:")
    print("  • Multi-Page PDF Text Mining & Normalization via PyPDF")
    print("  • Natural Speech Narration Engine via Google Text-to-Speech (gTTS)")
    print("  • Reading Time Estimation & Word Count Analytics")
    print("  • Export to Universal MP3 Digital Audio Format")
    print("=" * 76 + "\n")


def convert_sample():
    print("\n📖 CONVERTING SAMPLE PDF STORY TO AUDIOBOOK")
    print("=" * 65)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_pdf = os.path.join(base_dir, "sample_story.pdf")

    print(f"1. Extracting text from: {os.path.basename(sample_pdf)}...")
    text, pages = AudiobookConverter.extract_text(sample_pdf)
    metrics = AudiobookConverter.get_text_metrics(text)

    print(f"   • Extracted {pages} page(s) | {metrics['word_count']} words | {metrics['char_count']} chars")
    print(f"   • Estimated Audiobook Duration: ~{metrics['estimated_audio_minutes']} minutes\n")

    print("2. Synthesizing spoken audio narration via gTTS...")
    out_mp3 = os.path.join(base_dir, "audiobook_story.mp3")
    AudiobookConverter.convert_to_mp3(text, out_mp3)

    print(f"✅ Successfully exported audiobook to:")
    print(f"   file:///{out_mp3.replace(os.sep, '/')}\n")


def inspect_text():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_pdf = os.path.join(base_dir, "sample_story.pdf")
    text, pages = AudiobookConverter.extract_text(sample_pdf)

    print("\n📄 EXTRACTED PDF TEXT PREVIEW")
    print("=" * 65)
    print(text)
    print("=" * 65 + "\n")


def custom_convert():
    print("\n🎙️ CUSTOM PDF CONVERSION")
    print("=" * 65)
    path = input("Enter path to your PDF file: ").strip()
    if not os.path.exists(path):
        print(f"⚠️ File '{path}' not found.\n")
        return

    text, pages = AudiobookConverter.extract_text(path)
    metrics = AudiobookConverter.get_text_metrics(text)
    print(f"Extracted {pages} pages ({metrics['word_count']} words).")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_name = os.path.splitext(os.path.basename(path))[0] + "_audiobook.mp3"
    out_mp3 = os.path.join(base_dir, out_name)

    print("Synthesizing MP3 narration...")
    AudiobookConverter.convert_to_mp3(text, out_mp3)
    print(f"✅ Exported to: file:///{out_mp3.replace(os.sep, '/')}\n")


def run_automated_tests():
    """Verifies PDF text extraction, word metrics, and MP3 audio file generation."""
    print("\n🔍 Running Day 90 Automated Audiobook Converter Test Suite...")
    print("-" * 70)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_pdf = os.path.join(base_dir, "sample_story.pdf")

    # 1. Text extraction check
    text, pages = AudiobookConverter.extract_text(sample_pdf)
    assert pages >= 1
    assert "Python" in text
    assert len(text) > 100
    print(f" [PASS] 1. PyPDF text extraction verified: {pages} page(s) with {len(text)} characters.")

    # 2. Word count metrics check
    metrics = AudiobookConverter.get_text_metrics(text)
    assert metrics["word_count"] > 20
    assert metrics["estimated_audio_minutes"] > 0
    print(f" [PASS] 2. Reading metrics verified: {metrics['word_count']} words, ~{metrics['estimated_audio_minutes']} min duration.")

    # 3. Audio MP3 synthesis check
    test_mp3 = os.path.join(base_dir, "test_narration.mp3")
    AudiobookConverter.convert_to_mp3(text[:200], test_mp3)
    assert os.path.exists(test_mp3) and os.path.getsize(test_mp3) > 5000
    try:
        os.remove(test_mp3)
    except Exception:
        pass
    print(" [PASS] 3. Google TTS MP3 audio generation verified with valid binary size.")

    print("-" * 70)
    print("✨ ALL 3 TESTS PASSED! PDF to Audiobook Converter fully operational.\n")


def main():
    banner()
    while True:
        print("Select an option:")
        print("  1) 🎧 Convert Sample Story PDF to Spoken Audiobook (MP3)")
        print("  2) 📄 Preview Extracted Text & Reading Time Metrics")
        print("  3) 🎙️ Convert Custom Local PDF Document")
        print("  4) ✅ Run Automated Verification Suite (3 Unit Tests)")
        print("  5) 🚪 Exit")
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            convert_sample()
        elif choice == "2":
            inspect_text()
        elif choice == "3":
            custom_convert()
        elif choice == "4":
            run_automated_tests()
        elif choice in ("5", "exit", "quit", "q"):
            print("\n👋 Happy listening! Turn your books into audio 🎧\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 90 gracefully... Goodbye!\n")
