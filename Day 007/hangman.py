import random
from hangman_words import word_list
from hangman_art import stages, logo

print(logo)

choose_word = random.choice(word_list)
word = choose_word.lower()
#print(f"The word is {word}")
place_holder = ""

word_lenght = len(word)
print(word_lenght)
for position in range(word_lenght):
    place_holder += "_"
print(place_holder)

game_over = False
correct_guess = []
lives = 6

while not game_over:
    print(f"You have {lives} lives left")
    guess = input("Guess the letter: ").lower()

    if guess in correct_guess:
        print("+==================================================================+")
        print(f"| [!] NOTICE: You've already guessed '{guess}'. Try another letter! |")
        print("+==================================================================+")

    display = ""

    for letter in word:
        if letter == guess:
            display += letter
            if guess not in correct_guess:
                correct_guess.append(guess)
        elif letter in correct_guess:
            display += letter
        else:
            display += "_"

    print(display)

    if guess not in word:
        lives -= 1
        print(f"you guessed {guess}, that's not in the word. you have {lives} lives left")
        if lives == 0:
            game_over = True
            print("+==================================================================+")
            print(f"| [X] GAME OVER! The secret word was '{word.upper()}'. YOU LOSE!          |")
            print("+==================================================================+")

    if "_" not in display:
        game_over = True
        print("+==================================================================+")
        print("| [*] CONGRATULATIONS! You guessed the secret word! YOU WIN!       |")
        print("+==================================================================+")



    print(stages[6 - lives])
