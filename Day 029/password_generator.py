import random
import string

LETTERS = list(string.ascii_letters)
NUMBERS = list(string.digits)
SYMBOLS = ["!", "#", "$", "%", "&", "(", ")", "*", "+", "@", "^", "?"]


def generate_secure_password(nr_letters: int = 8, nr_symbols: int = 4, nr_numbers: int = 4) -> str:
    """Generates a high-entropy random password using letters, symbols, and numbers."""
    password_letters = [random.choice(LETTERS) for _ in range(nr_letters)]
    password_symbols = [random.choice(SYMBOLS) for _ in range(nr_symbols)]
    password_numbers = [random.choice(NUMBERS) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    return "".join(password_list)


if __name__ == "__main__":
    sample_pwd = generate_secure_password()
    print(f"Generated sample password: {sample_pwd}")
