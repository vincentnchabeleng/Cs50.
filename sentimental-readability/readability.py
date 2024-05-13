import cs50

# Function to calculate Coleman-Liau index
def calculate_index(letters, words, sentences):
    L = (letters / words) * 100
    S = (sentences / words) * 100
    return round(0.0588 * L - 0.296 * S - 15.8)

# Prompt the user for input
text = cs50.get_string("Text: ")

# Initialize counters for letters, words, and sentences
letters = words = sentences = 0

# Loop through each character in the input text
for char in text:
    # Count letters
    if char.isalpha():
        letters += 1
    # Count words by counting spaces
    elif char.isspace():
        words += 1
    # Count sentences by detecting end of sentence punctuation
    elif char in ['.', '?', '!']:
        sentences += 1

# Add one to words for the last word
words += 1

# Calculate the Coleman-Liau index
index = calculate_index(letters, words, sentences)

# Determine and print the grade level based on the index
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
