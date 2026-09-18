"""
Day 30 - NATO Phonetic Alphabet (Version 2 - Resilient with KeyError Exception Handling)
Demonstrates using try/except to catch invalid non-alphabetic inputs and re-prompting gracefully.
"""

import os
import sys

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Standard NATO Phonetic Dictionary
NATO_DICT = {
    'A': 'Alfa', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo',
    'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliet',
    'K': 'Kilo', 'L': 'Lima', 'M': 'Mike', 'N': 'November', 'O': 'Oscar',
    'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
    'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray', 'Y': 'Yankee',
    'Z': 'Zulu'
}


def load_nato_dictionary():
    """Attempts to load NATO alphabet from CSV if available, with in-memory fallback."""
    csv_paths = [
        os.path.join(os.path.dirname(__file__), "..", "Day 26", "nato_phonetic_alphabet.csv"),
        os.path.join(os.path.dirname(__file__), "nato_phonetic_alphabet.csv")
    ]
    for path in csv_paths:
        if os.path.exists(path):
            try:
                import pandas as pd
                df = pd.read_csv(path)
                return {row.letter: row.code for (_, row) in df.iterrows()}
            except Exception:
                pass
    return NATO_DICT


def generate_phonetic_words(user_word: str, phonetic_dict: dict) -> list:
    """
    Translates a word into phonetic codes.
    Raises KeyError if any character cannot be mapped.
    """
    cleaned_word = user_word.strip().upper()
    if not cleaned_word:
        raise ValueError("Input string cannot be empty!")
    return [phonetic_dict[letter] for letter in cleaned_word]


def run_nato_encoder_resilient():
    """
    Loops interactively, prompting the user for a word and catching KeyError.
    Gracefully handles KeyboardInterrupt and EOFError.
    """
    phonetic_dict = load_nato_dictionary()

    print("\n" + "=" * 65)
    print(" 📡 NATO PHONETIC ENCODER V2 (WITH KEYERROR EXCEPTION RECOVERY)")
    print("=" * 65)
    print("Type any English word to convert it to NATO code words.")
    print("Type 'exit' or 'q' to return to menu.\n")

    while True:
        try:
            word = input("👉 Enter a word: ").strip()
            if not word:
                print("⚠️ Please enter at least one word!\n")
                continue
            if word.lower() in ("exit", "q", "quit"):
                print("👋 Returning to main menu...\n")
                break

            output_list = generate_phonetic_words(word, phonetic_dict)

        except KeyError as err_key:
            print(f"❌ KeyError: {err_key} is not a valid alphabet letter!")
            print("⚠️ Sorry, only letters in the alphabet please. Numbers and symbols are not allowed.\n")

        except ValueError as err_val:
            print(f"⚠️ {err_val}\n")

        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Input cancelled. Exiting NATO encoder.\n")
            break

        else:
            print(f"\n✅ Phonetic Translation for '{word.upper()}':")
            print("   " + " ➔ ".join(output_list))
            print(f"   Formatted List: {output_list}\n")


if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    run_nato_encoder_resilient()
