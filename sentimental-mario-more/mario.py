from cs50 import get_int

# Prompt the user to enter the height until a valid input is recieved
height = 0
while height < 1 or height > 8:
    height = get_int("Height: ")

# Iterate over each row of the pyramid
for row in range(height):
    # Print spaces for the left side of the left-aligned pyramid
    print((height - 1 - row) * " ", end = "")

    # Print hashes for the left side of the left-aligned pyramid
    print((row + 1) * "#", end = "")

    # Print spaces between the two pyramids
    print("  ", end = "")

    # Print hashes for the right side of the right-aligned pyramid
    print((row + 1) * "#")
