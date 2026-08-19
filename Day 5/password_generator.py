import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the Password Generator!")
number_of_letters = int(input("How many letters would you like in your password? "))
number_of_numbers = int(input("How many numbers would you like in your password? "))
number_of_symbols = int(input("How many symbols would you like in your password? "))

password_list = []

for i in range(number_of_letters):
    password_list.append(random.choice(letters))
    
for i in range(number_of_numbers):
    password_list.append(random.choice(numbers))

for i in range(number_of_symbols):
    password_list.append(random.choice(symbols))

random.shuffle(password_list)

password = "".join(password_list)

print(f"Your randomly generated password is {password}")