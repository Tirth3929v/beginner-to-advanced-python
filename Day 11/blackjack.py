import random
import art

def deal_card():
    """Returns a random card from the deck."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def calculate_score(cards):
    """Take a list of cards and return the score calculated from the cards."""
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # 0 represents Blackjack
    
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
        
    return sum(cards)

def display_hand(name, cards, score, hide_second=False):
    """Formats and prints cards nicely with styled text and score."""
    if hide_second:
        print(f"🃏 {name}'s first card: [{cards[0]}]  (Score: ?)")
    else:
        score_str = "BLACKJACK! 21 🎰" if score == 0 else str(score)
        cards_formatted = ", ".join([str(c) if c != 11 else "11(Ace)" for c in cards])
        print(f"🎴 {name}'s cards: [{cards_formatted}]  |  Total Score: {score_str}")

def compare(user_score, computer_score):
    """Compares user and computer scores and returns the match result with interesting commentary."""
    if user_score == computer_score:
        statement = random.choice(art.draw_statements)
        return f"\n🤝 It's a DRAW! 🙃\n{statement}"
    elif computer_score == 0:
        return f"\n😱 LOSE! Dealer hit a Blackjack! 🎰\n{random.choice(art.loss_statements)}"
    elif user_score == 0:
        return f"\n😎 WIN! You hit a BLACKJACK! ⚡\n{random.choice(art.blackjack_statements)}"
    elif user_score > 21:
        return f"\n💥 BUST! You went over 21! You lose 😤\n{random.choice(art.loss_statements)}"
    elif computer_score > 21:
        return f"\n💥 DEALER BUST! Opponent went over 21! You WIN! 😎\n{random.choice(art.win_statements)}"
    elif user_score > computer_score:
        return f"\n🏆 YOU WIN! You outscored the dealer! 😎\n{random.choice(art.win_statements)}"
    else:
        return f"\n😤 YOU LOSE! Dealer outscored your hand. 📉\n{random.choice(art.loss_statements)}"

def play_game():
    print(art.logo)
    print(art.cards_banner)
    print("Welcome to High Stakes Blackjack! 🎲\n" + "-"*55)
    
    user_cards = []
    computer_cards = []
    user_score = -1
    computer_score = -1
    is_game_over = False

    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())

    while not is_game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)

        display_hand("Your hand", user_cards, user_score)
        display_hand("Dealer", computer_cards, computer_score, hide_second=True)

        if user_score == 0 or computer_score == 0 or user_score > 21:
            is_game_over = True
        else:
            user_should_deal = input("\n👉 Type 'y' to hit (get another card), type 'n' to stand (pass): ").lower()
            if user_should_deal == 'y':
                drawn_card = deal_card()
                user_cards.append(drawn_card)
                print(f"✨ You drew a [{drawn_card}]!")
            else:
                is_game_over = True
            print("-" * 55)

    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)

    print("\n" + "="*55)
    print("📊 FINAL RESULTS")
    print("="*55)
    display_hand("Your final hand", user_cards, user_score)
    display_hand("Dealer's final hand", computer_cards, computer_score)
    
    print(compare(user_score, computer_score))
    print("="*55 + "\n")

if __name__ == "__main__":
    play_game()
    while input("🎰 Do you want to play another game of Blackjack? Type 'y' or 'n': ").lower() == 'y':
        print("\n" * 5)
        play_game()
