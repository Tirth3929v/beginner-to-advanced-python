import random
import sys
from art import logo, vs
from game_data import data

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def format_data(account):
    """Format account data into an engaging string with emojis."""
    account_name = account['name']
    account_description = account['description']
    account_country = account['country']
    return f"{account_name}, a {account_description}, from {account_country} 🌍"


def check_answer(guess, a_followers, b_followers):
    """Take the user guess and follower counts and return if they got it right."""
    if a_followers > b_followers:
        return guess == "a"
    else:
        return guess == "b"


def game():
    print(logo)
    score = 0
    game_should_continue = True
    account_b = random.choice(data)

    while game_should_continue:
        # Move B to A, pick a new B
        account_a = account_b
        account_b = random.choice(data)

        while account_a == account_b:
            account_b = random.choice(data)

        print(f"\n🅰️  Option A: {format_data(account_a)}")
        print(vs)
        print(f"🅱️  Option B: {format_data(account_b)}")

        guess = input("\n🤔 Who has more followers? Type 'A' or 'B': ").strip().lower()

        a_follower_count = account_a["follower_count"]
        b_follower_count = account_b["follower_count"]
        is_correct = check_answer(guess, a_follower_count, b_follower_count)

        if is_correct:
            score += 1
            print(f"\n🎉 Bingo! You got it right! 🔥 Current Score: {score} 🏆")
            print("─" * 70)
        else:
            game_should_continue = False
            print(f"\n❌ Oops! That's incorrect.")
            print(f"📊 {account_a['name']} has {a_follower_count}M followers vs {account_b['name']} with {b_follower_count}M followers.")
            print(f"💥 Game Over! Final Score: {score} 🏆\n" + "═" * 70)


def play():
    while True:
        game()
        play_again = input("\n🔄 Would you like to play again? (Type 'y' for Yes / 'n' for No): ").strip().lower()
        if play_again not in ['y', 'yes']:
            print("\n👋 Thanks for playing Higher Lower! See you next time! ✨\n")
            break


if __name__ == "__main__":
    play()
