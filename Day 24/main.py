import os
import sys
from art import logo

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Constants for File Paths
PLACEHOLDER = "[name]"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMES_PATH = os.path.join(BASE_DIR, "Input", "Names", "invited_names.txt")
TEMPLATE_PATH = os.path.join(BASE_DIR, "Input", "Letters", "starting_letter.txt")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output", "ReadyToSend")


def generate_mail_merge():
    """Reads starting letter template and invited names, replacing placeholders to generate personalized letters."""
    print(logo)
    print("Welcome to Day 24 - Mail Merge File Automation Engine! ✉️🤖\n")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Read invited guest names
    if not os.path.exists(NAMES_PATH):
        print(f"❌ Error: Names file not found at '{NAMES_PATH}'")
        return

    with open(NAMES_PATH, "r", encoding="utf-8") as names_file:
        names = [name.strip() for name in names_file.readlines() if name.strip()]

    # 2. Read starting letter template
    if not os.path.exists(TEMPLATE_PATH):
        print(f"❌ Error: Template letter file not found at '{TEMPLATE_PATH}'")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as template_file:
        letter_template = template_file.read()

    print(f"📋 Found {len(names)} invited guests in invitation list.")
    print("🔄 Generating personalized letters...\n" + "─" * 60)

    # 3. Replace placeholder and save each personalized letter file
    generated_files = []
    for name in names:
        personalized_letter = letter_template.replace(PLACEHOLDER, name)
        output_file_name = f"letter_for_{name.lower().replace(' ', '_')}.txt"
        output_file_path = os.path.join(OUTPUT_DIR, output_file_name)

        with open(output_file_path, "w", encoding="utf-8") as completed_letter:
            completed_letter.write(personalized_letter)

        generated_files.append(output_file_name)
        print(f"  ✅ Generated: {output_file_name}")

    print("─" * 60)
    print(f"\n🎉 Successfully created {len(generated_files)} personalized letters in '{OUTPUT_DIR}'! 📬✨\n")


if __name__ == "__main__":
    generate_mail_merge()
