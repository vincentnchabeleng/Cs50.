books = []

# Add hree books  to shelf
for i in range(3):
    book = dict()
    book["Author"] = input("Enter the name of the author:")
    book["Title"] = input("Enter title:")
    book.append(book)

# Print list of the books
for book in books:
    print(book)
    print(f"{book["Author"]} wrote {book["Title"]}.")
    print(f"Author = {book["Author"]}.")
    print(f"Title = {book["Title"]}.")

