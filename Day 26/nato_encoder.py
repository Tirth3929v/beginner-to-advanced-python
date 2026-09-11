import csv
import os
import sys

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "nato_phonetic_alphabet.csv")


def load_phonetic_dict() -> dict[str, str]:
    """Reads NATO phonetic CSV and creates a dictionary mapping using comprehension."""
    phonetic_dict = {}
    if not os.path.exists(CSV_FILE):
        return phonetic_dict

    try:
        import pandas as pd
        data = pd.read_csv(CSV_FILE)
        # Dictionary Comprehension with pandas DataFrame
        phonetic_dict = {row.letter: row.code for (_, row) in data.iterrows()}
    except Exception:
        # Dictionary Comprehension with standard library CSV reader fallback
        with open(CSV_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            phonetic_dict = {row["letter"].strip().upper(): row["code"].strip() for row in reader}

    return phonetic_dict


def encode_word(word: str, phonetic_dict: dict[str, str]) -> list[str]:
    """Translates a word into its phonetic equivalent list using List Comprehension."""
    # List Comprehension converting letters to phonetic codes
    return [phonetic_dict[letter] for letter in word.upper() if letter.isalpha()]


def run_nato_encoder():
    """Interactive loop for phonetic encoding with error handling."""
    phonetic_dict = load_phonetic_dict()
    if not phonetic_dict:
        print("❌ Error: NATO dataset not loaded.")
        return

    print("\n🔤 NATO Phonetic Alphabet Encoder")
    print("─" * 50)
    print("Type any word or phrase to convert it to official aviation phonetic words.")
    print("Type 'exit' to return to menu.\n")

    while True:
        try:
            user_input = input("👉 Enter a word: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n↩️ Returning to menu...\n")
            break

        if user_input.lower() in ["exit", "q", "quit"]:
            break

        if not user_input:
            continue

        try:
            # Strict validation using List Comprehension
            result = [phonetic_dict[letter] for letter in user_input.upper()]
            print(f"✨ Phonetic Code: {' - '.join(result)}\n")
        except KeyError:
            print("⚠️  Sorry, only letters in the English alphabet please (no numbers or symbols).\n")


if __name__ == "__main__":
    try:
        run_nato_encoder()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!\n")

