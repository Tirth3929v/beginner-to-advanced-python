import art

print(art.logo)
print("Welcome to the Caesar Cipher!\n")

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def caeser_cipher(original_text, shift_amount, encode_or_decode):
    cipher_text = ""
    if encode_or_decode == "decode":
        shift_amount *= -1
    
    for letter in original_text:
        if letter not in alphabet:
            cipher_text += letter
        else:
            shifted_position = alphabet.index(letter) + shift_amount
            shifted_position %= len(alphabet)
            cipher_text += alphabet[shifted_position]
            
    print(f"\n---> The {encode_or_decode}d text is: {cipher_text} <---")

should_continue = True
while should_continue:
    direction = input("\nType 'encode' to encrypt, type 'decode' to decrypt:\n> ").lower()
    text = input("Type your message:\n> ").lower()
    shift = int(input("Type the shift number:\n> "))
    
    caeser_cipher(original_text=text, shift_amount=shift, encode_or_decode=direction)
    
    restart = input("\nType 'yes' if you want to go again. Otherwise, type 'no':\n> ").lower()
    if restart == "no":
        should_continue = False
        print("\nGoodbye! Have a great day!")