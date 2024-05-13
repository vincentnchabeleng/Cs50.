import cs50

# Prompt the user for credit card number
while True:
    credit_card = cs50.get_int("Enter your credit card number: ")
    if credit_card > 0:
        break
    else:
        print("Please enter a positive number.")

# Convert the credit card number to a string
card_number = str(credit_card)
length = len(card_number)
sum = 0

# Calculate the checksum
for i in range(length - 1, -1, -1):
    digit = int(card_number[i])
    # Double every other digit starting from the second-to-last
    if (length - i) % 2 == 0:
        digit *= 2
        # Add the digits of the doubled number to the sum
        sum += digit // 10 + digit % 10
    else:
        # Add the digit to the sum
        sum += digit

# Check if the checksum is valid and determine the card type
if sum % 10 == 0:
    prefix = int(card_number[:2])
    # Check for AMEX card
    if length == 15 and (prefix == 34 or prefix == 37):
        print("AMEX")
    # Check for MASTERCARD
    elif length == 16 and 51 <= prefix <= 55:
        print("MASTERCARD")
    # Check for VISA
    elif (length == 13 or length == 16) and card_number[0] == '4':
        print("VISA")
    else:
        # If none of the conditions are met, the card is invalid
        print("INVALID")
else:
    # If the checksum is not divisible by 10, the card is invalid
    print("INVALID")
