from cs50 import get_float

# Prompt the user to enter the amount of change owed until a non-negative value is entered
while True:
    change = get_float("Change: ")
    if change >= 0:
        break

# Convert dollars to cents
cents = round(change * 100)

# Initialize a variable to count the total number of coins
coins = 0
# Define the denominations of coins
denominations = [25, 10, 5, 1]

# Iterate over each denomination of coin
for denomination in denominations:
    # Calculate the number of coins of the current denomination
    coins += cents // denomination
    # Update the remaining cents after using the current denomination
    cents %= denomination

# Print the total number of coins required to make the change
print(coins)
