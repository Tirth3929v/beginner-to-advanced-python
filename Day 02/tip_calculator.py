print("Welcome to the Tip Calculator\n")
total_bill = float(input("What was the total bill? $ "))
tip_percentage = int(input("What percentage tip would you like to give? 10, 12 or 15: "))
people = int(input("How many people to split the bill? "))
tip_amount = total_bill * (tip_percentage / 100)
total_amount = total_bill + tip_amount
split_amount = total_amount / people
final_amount = round(split_amount, 2)
print(f"Each person should pay: ${final_amount}")