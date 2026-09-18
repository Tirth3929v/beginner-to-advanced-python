"""
Day 81: Text-to-Morse Code Converter
Interactive Translation & Telegraphy Audio Synthesizer CLI
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
from morse_engine import MorseEngine, MORSE_CODE_DICT


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 81: INTERNATIONAL MORSE CODE ENGINE & AUDIO SYNTHESIZER")
    print(" 📚 Phase 4: Professional Portfolio Projects | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Core Telegraphy Features:")
    print("  • ITU-R Standard Morse Code Specification (Alphanumerics & Symbols)")
    print("  • Bidirectional Translation: Text -> Dots/Dashes & Morse -> Plaintext")
    print("  • Pure Python 800Hz PCM Sine Wave Synthesis (Zero third-party audio deps)")
    print("  • Real-time Telegraphy Sound Generation & 16-bit WAV Exporter")
    print("=" * 76 + "\n")


def encode_cli():
    print("\n📝 TEXT TO MORSE ENCODER")
    print("=" * 60)
    text = input("Enter text to transmit: ").strip()
    if not text:
        text = "SOS MAYDAY WE NEED PYTHON DEVELOPERS"

    morse = MorseEngine.encode(text)
    print(f"\n📡 Transmitted Plaintext: \033[92m{text.upper()}\033[0m")
    print(f"📻 Encoded Morse Code:    \033[93m{morse}\033[0m\n")

    play = input("Synthesize and export 800Hz audio WAV? (y/n, default y): ").strip().lower()
    if not play or play.startswith("y"):
        wav_file = MorseEngine.synthesize_wav(morse, "transmission.wav")
        print(f"✅ Exported telegraph audio to:")
        print(f"   file:///{wav_file.replace(os.sep, '/')}\n")


def decode_cli():
    print("\n📻 MORSE TO TEXT DECODER")
    print("=" * 60)
    print("Tip: Use spaces between letters and ' / ' between words.")
    morse = input("Enter Morse Code (e.g. '... --- ...'): ").strip()
    if not morse:
        morse = "... --- ... / -... ..- .. .-.. -.. / .. -. / .--. -.-- - .... --- -."

    decoded = MorseEngine.decode(morse)
    print(f"\n📡 Input Morse:   \033[93m{morse}\033[0m")
    print(f"📄 Decoded Text:  \033[92m{decoded}\033[0m\n")


def export_custom_audio():
    print("\n🎵 AUDIO WAV SYNTHESIZER")
    print("=" * 60)
    text = input("Enter phrase for audio synthesis: ").strip()
    if not text:
        text = "CQ CQ CQ DE PYTHON"
    morse = MorseEngine.encode(text)
    wpm_str = input("Transmission Speed (WPM, default 15): ").strip()
    wpm = int(wpm_str) if wpm_str.isdigit() else 15

    wav_file = MorseEngine.synthesize_wav(morse, f"morse_{wpm}wpm.wav", wpm=wpm)
    print(f"\n✅ Synthesized {wpm} WPM telegraph audio ({len(morse)} symbols):")
    print(f"   file:///{wav_file.replace(os.sep, '/')}\n")


def display_reference():
    print("\n📖 INTERNATIONAL MORSE CODE REFERENCE CHART")
    print("=" * 70)
    items = list(MORSE_CODE_DICT.items())
    for i in range(0, len(items), 4):
        batch = items[i:i+4]
        row_str = "   ".join([f" \033[96m{k}\033[0m: {v:<7}" for k, v in batch])
        print(f"  {row_str}")
    print("=" * 70 + "\n")


def run_automated_tests():
    """Validates bidirectional encoding, punctuation, and WAV audio binary generation."""
    print("\n🔍 Running Day 81 Automated Morse Code Verification Suite...")
    print("-" * 70)

    # 1. Basic encoding test
    sos = MorseEngine.encode("SOS")
    assert sos == "... --- ...", f"Expected '... --- ...', got {sos}"
    print(" [PASS] 1. Flagship signal SOS correctly encoded.")

    # 2. Words spacing test
    phrase = "HELLO WORLD"
    morse_phrase = MorseEngine.encode(phrase)
    assert " / " in morse_phrase, "Words must be delimited by ' / '."
    print(f" [PASS] 2. Multi-word phrase encoding verified: '{phrase}' -> '{morse_phrase}'.")

    # 3. Decoding fidelity
    decoded = MorseEngine.decode(morse_phrase)
    assert decoded == phrase, f"Expected '{phrase}', got '{decoded}'"
    print(" [PASS] 3. Bidirectional decoding parity: Encoded and decoded strings match 100%.")

    # 4. Punctuation handling
    punct = "TEST 123!?"
    punct_morse = MorseEngine.encode(punct)
    assert MorseEngine.decode(punct_morse) == punct
    print(" [PASS] 4. Numbers and punctuation (123!?) round-trip translation verified.")

    # 5. Audio WAV synthesis test
    wav_path = MorseEngine.synthesize_wav("... --- ...", "test_sos.wav")
    assert os.path.exists(wav_path) and os.path.getsize(wav_path) > 1000
    try:
        os.remove(wav_path)
    except Exception:
        pass
    print(" [PASS] 5. 800Hz PCM Sine Wave WAV binary synthesis verified.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Morse Code Engine fully operational.\n")


def main():
    banner()
    while True:
        print("Select an option:")
        print("  1) 📝 Encode Text to Morse Code (with audio export)")
        print("  2) 📻 Decode Morse Code to Plaintext")
        print("  3) 🎵 Synthesize & Export Custom Speed Morse WAV")
        print("  4) 📖 View International Morse Code Reference Chart")
        print("  5) ✅ Run Automated Verification Suite (5 Unit Tests)")
        print("  6) 🚪 Exit")
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            encode_cli()
        elif choice == "2":
            decode_cli()
        elif choice == "3":
            export_custom_audio()
        elif choice == "4":
            display_reference()
        elif choice == "5":
            run_automated_tests()
        elif choice in ("6", "exit", "quit", "q"):
            print("\n👋 73 and 88! Happy Telegraphy! 📻\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-6.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 81 gracefully... Goodbye!\n")
