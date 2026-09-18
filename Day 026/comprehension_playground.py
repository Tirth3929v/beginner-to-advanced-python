import random
import sys
from nato_encoder import load_phonetic_dict

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def run_comprehension_demos():
    """Demonstrates list, dictionary, and conditional comprehensions with live execution."""
    print("\n🧪 Python Comprehension Playground Demos")
    print("═" * 60)

    # 1. List Comprehensions: Squaring & Even Filtering
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    squared_evens = [n ** 2 for n in numbers if n % 2 == 0]
    print("1️⃣ List Comprehension (Squared Evens):")
    print(f"   Original Numbers: {numbers}")
    print(f"   [n**2 for n in numbers if n % 2 == 0] -> {squared_evens}\n")

    # 2. Dictionary Comprehensions: Word Lengths
    sentence = "The quick brown fox jumps over the lazy dog"
    words = sentence.split()
    word_lengths = {word.lower(): len(word) for word in words}
    print("2️⃣ Dictionary Comprehension (Word Lengths):")
    print(f"   Sentence: '{sentence}'")
    print(f"   {{word: len(word) for word in words}} ->")
    print(f"   {word_lengths}\n")

    # 3. Conditional Dictionary Comprehension: Passing Students
    student_scores = {
        "Alex": 88,
        "Beth": 62,
        "Caroline": 95,
        "Dave": 54,
        "Eleanor": 77,
        "Freddie": 45
    }
    passed_students = {student: score for (student, score) in student_scores.items() if score >= 60}
    print("3️⃣ Conditional Dict Comprehension (Passing Students >= 60):")
    print(f"   All Scores: {student_scores}")
    print(f"   {{s: score for s, score in scores.items() if score >= 60}} ->")
    print(f"   {passed_students}\n")

    # 4. Temperature Conversion (Celsius to Fahrenheit)
    weather_c = {"Monday": 12, "Tuesday": 14, "Wednesday": 15, "Thursday": 14, "Friday": 21, "Saturday": 22, "Sunday": 24}
    weather_f = {day: round((temp_c * 9/5) + 32, 1) for (day, temp_c) in weather_c.items()}
    print("4️⃣ Dict Comprehension (Weather °C to °F):")
    print(f"   Celsius: {weather_c}")
    print(f"   Fahrenheit: {weather_f}")
    print("═" * 60 + "\n")


def run_nato_quiz():
    """Interactive quiz testing user knowledge of the NATO phonetic alphabet."""
    phonetic_dict = load_phonetic_dict()
    if not phonetic_dict:
        print("❌ Error: NATO dataset not loaded.")
        return

    letters = list(phonetic_dict.keys())
    score = 0
    total_rounds = 5

    print("\n🎯 NATO Phonetic Alphabet Quick Quiz (5 Questions)")
    print("─" * 55)
    print("Test your aviation phonetic knowledge! Type the code word for each letter.\n")

    try:
        sample_letters = random.sample(letters, total_rounds)
        for i, letter in enumerate(sample_letters, 1):
            correct_code = phonetic_dict[letter]
            user_guess = input(f"Q{i}. What is the NATO phonetic word for letter '{letter}'? : ").strip()

            if user_guess.lower() == correct_code.lower():
                score += 1
                print(f"   ✅ Correct! '{letter}' is for {correct_code}.\n")
            else:
                print(f"   ❌ Incorrect! '{letter}' is for {correct_code}.\n")

        percentage = (score / total_rounds) * 100
        print(f"🏆 Quiz Finished! Final Score: {score}/{total_rounds} ({percentage:.0f}%)\n")
    except (KeyboardInterrupt, EOFError):
        print("\n\n↩️ Quiz cancelled. Returning to menu...\n")


if __name__ == "__main__":
    try:
        run_comprehension_demos()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!\n")

