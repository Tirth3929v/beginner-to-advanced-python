import os
import art

def clear_screen():
    """Clears the console screen for modern silent bidding privacy."""
    os.system('cls' if os.name == 'nt' else 'clear')

def find_highest_bidder(bidding_dictionary):
    """Finds and displays the highest bidder from the bids dictionary."""
    highest_bid = 0
    winner = ""
    
    for bidder in bidding_dictionary:
        bid_amount = bidding_dictionary[bidder]
        if bid_amount > highest_bid:
            highest_bid = bid_amount
            winner = bidder
            
    print("\n" + "=" * 55)
    print("        *** AUCTION COMPLETED & RESULTS ARE IN! ***")
    print("=" * 55)
    print(f"  WINNER: {winner.upper()}")
    print(f"  WINNING BID: ${highest_bid:,}")
    print("=" * 55 + "\n")

def main():
    clear_screen()
    print(art.logo)
    print("      Welcome to the Secret Silent Auction Program!")
    print("=" * 55)
    
    bids = {}
    continue_bidding = True

    while continue_bidding:
        name = input("\n[+] Enter your name: ").strip()
        while not name:
            name = input("[!] Name cannot be empty. Enter your name: ").strip()
            
        while True:
            try:
                price = int(input("[$] Enter your bid amount: $"))
                if price <= 0:
                    print("[!] Bid amount must be greater than $0.")
                    continue
                break
            except ValueError:
                print("[!] Invalid input! Please enter a valid whole number.")
                
        bids[name] = price
        
        while True:
            should_continue = input("\n[?] Are there any other bidders? (yes/no): ").strip().lower()
            if should_continue in ["yes", "no"]:
                break
            print("[!] Invalid response! Please type 'yes' or 'no'.")
            
        if should_continue == "no":
            continue_bidding = False
            clear_screen()
            find_highest_bidder(bids)
        elif should_continue == "yes":
            clear_screen()
            print(art.logo)
            print("   Next bidder's turn! Please pass the device.")
            print("=" * 55)

if __name__ == "__main__":
    main()