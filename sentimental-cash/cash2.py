from cs50 import get_float

# Prompt the user to enter the amount of change owed until a non-negative value is entered
while True:
    change = get_float("Change: ")
    if change >= 0:
        break

# Convert dollars to cents
cents = round(change * 100)

# Initialize a dictionary to store the count of each coin denomination
coin_counts = {25: 0, 10: 0, 5: 0, 1: 0}

# Iterate over each denomination of coin
for denomination in coin_counts:
    # Calculate the number of coins of the current denomination
    coin_counts[denomination] += cents // denomination
    # Update the remaining cents after using the current denomination
    cents %= denomination

# Print the count of each coin denomination
for denomination, count in coin_counts.items():
    print(f"Number of {denomination}-cent coin(s): {count}")

# Calculate and print the total number of coins
total_coins = sum(coin_counts.values())
print("Total number of coins:", total_coins)
