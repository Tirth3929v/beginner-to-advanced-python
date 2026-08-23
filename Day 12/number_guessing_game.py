import sys
import io
from random import randint
from art import logo

# Fix UTF-8 encoding output on Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EASY_LIVES = 10
HARD_LIVES = 5

def check_answer(guess, answer, attempts):
    """Checks answer against guess and returns updated attempts."""
    if guess > answer:
        print("  📈 [TOO HIGH] >>> Try a lower number!")
        return attempts - 1
    elif guess < answer:
        print("  📉 [TOO LOW]  <<< Try a higher number!")
        return attempts - 1
    else:
        print(f"\n  🏆 [VICTORY!] 🎉 Spot on! You guessed the secret number {answer}!")
        return attempts

def set_difficulty():
    while True:
        difficulty = input("\n⚙️ Choose difficulty | Type 'easy' (10 attempts 🟢) or 'hard' (5 attempts 🔴): ").strip().lower()
        if difficulty == 'easy':
            return EASY_LIVES
        elif difficulty == 'hard':
            return HARD_LIVES
        else:
            print("  ⚠️ Invalid choice. Please enter 'easy' or 'hard'.")

def game():
    print(logo)
    print("==========================================================")
    print("   🎮 WELCOME TO THE NUMBER GUESSING GAME! 🎲")
    print("   🔮 I am thinking of a secret number between 1 and 100.")
    print("==========================================================")

    answer = randint(1, 100)
    attempts = set_difficulty()

    guess = 0
    while guess != answer:
        print(f"\n----------------------------------------------------------")
        print(f"  ❤️ [STATUS] Attempts remaining: {attempts}")
        
        try:
            guess = int(input("  🔍 Make a guess: "))
        except ValueError:
            print("  ⚠️ Invalid input! Please enter a valid whole number.")
            continue

        attempts = check_answer(guess, answer, attempts)

        if attempts == 0 and guess != answer:
            print(f"\n----------------------------------------------------------")
            print(f"  💀 [GAME OVER] You've run out of guesses!")
            print(f"  💡 The secret number was: {answer}")
            return
        elif guess != answer:
            print("  🤔 Keep guessing!")

def main():
    while True:
        game()
        choice = input("\n  🔄 Do you want to play again? Type 'y' for Yes or 'n' for No: ").strip().lower()
        if choice != 'y':
            print("\n  👋 [THANK YOU FOR PLAYING!] Goodbye! ✨\n")
            break

if __name__ == "__main__":
    main()
