import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, redirect, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter for USD formatting
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Homepage route
@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user = session["user_id"]

    # Get the user's stock purchases and cash balance
    purchases = db.execute("SELECT symbol, SUM(shares) AS totalShares FROM purchases WHERE user_id = (?) GROUP BY symbol HAVING totalShares > 0",user)
    userCashDb = db.execute("SELECT cash FROM users WHERE id = ?", user)
    userCash = userCashDb[0]["cash"] if userCashDb else 0

    # Calculate total portfolio value
    total = userCash
    for row in purchases:
        symbol = row["symbol"]
        quote = lookup(symbol)
        row["name"] = quote["symbol"]
        row["price"] = quote["price"]
        row["value"] = row["price"] * row["totalShares"]
        total += row["value"]
        row["total"] = row["price"] * row["totalShares"]

    # Render the index.html template with portfolio information
    return render_template("index.html", stocks=purchases, cash=usd(userCash), total=usd(total))

# Buy stocks route
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # Check if user ID is present in the session
    user_id = session.get("user_id")
    if user_id is None:
        # Return an apology if user ID is not found in the session
        return apology("User ID not found in session", 400)

    if request.method == "POST":
        # Get symbol and shares from the form data
        symbol = request.form.get("symbol")
        shares_str = request.form.get("shares")

        # Validate symbol and shares inputs
        if not symbol or not shares_str:
            return apology("Please provide both symbol and shares", 400)

        try:
            shares = int(shares_str)
            if shares <= 0:
                return apology("Shares must be a positive integer", 400)
        except ValueError:
            return apology("Shares must be a valid number", 400)

        # Lookup the stock symbol to get its current price
        quote = lookup(symbol)
        if not quote:
            return apology("Symbol not found", 400)

        price = quote["price"]
        total_cost = price * shares

        # Retrieve user information from the database
        user = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=user_id)[0]
        if not user:
            return apology("User not found", 400)

        if user["cash"] < total_cost:
            return apology("Insufficient funds", 400)

        # Update user's cash balance after buying stocks
        db.execute("UPDATE users SET cash = cash - :total WHERE id = :user_id", total=total_cost, user_id=user_id)

        # Record the purchase in the 'purchases' table
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price, total) VALUES (:user_id, :symbol, :shares, :price, :total)",
                   user_id=user_id, symbol=symbol, shares=shares, price=price, total=total_cost)

        # Record the buy transaction in the 'history' table
        db.execute("INSERT INTO history (user_id, symbol, shares, price, transaction_type, total) VALUES (:user_id, :symbol, :shares, :price, 'Buy', :total)",
                   user_id=user_id, symbol=symbol, shares=shares, price=price, total=total_cost)
        print("total:" , total_cost)

        # Flash success message
        flash("Stock purchase successful!", "success")

        # Redirect user to the homepage after successful purchase
        return redirect("/")
    else:
        # Render the buy.html template for displaying the form to buy stocks
        return render_template("buy.html")

# Transaction history route
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Get the current user's ID from the session
    user = session["user_id"]
    # Retrieve the user's transaction history from the database
    transactions = db.execute("SELECT * FROM history WHERE user_id = :user ORDER BY timestamp DESC;", user=user)
    # Render the history.html template to display the transaction history
    return render_template("history.html", transactions=transactions)

# User login route
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()  # Forget any user_id

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Query the database to check if the user exists
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        # Check if the username exists and the password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Invalid username and/or password", 403)

        # Remember user login by storing user ID in the session
        session["user_id"] = rows[0]["id"]
        session["username"] = username
        return redirect("/")
    else:
        # Render the login.html template for displaying the login form
        return render_template("login.html")

# User logout route
@app.route("/logout")
def logout():
    """Log user out"""
    # Clear the session to forget the user's login information
    session.clear()
    # Redirect the user to the homepage or login page
    return redirect("/")

# Get stock quote route
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":  # Check if the request method is POST
        symbol = request.form.get("symbol")  # Get the symbol from the form data
        if not symbol or not lookup(symbol):  # Check if the symbol is valid
            return apology("Invalid symbol", 400)  # Return an apology if the symbol is invalid
        return render_template("quoted.html", quote=lookup(symbol))  # Render the quoted.html template with the stock quote
    else:
        return render_template("quote.html")  # Render the quote.html template for displaying the form

# Change password route
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    session.clear()  # Clear any existing session data

    if request.method == "POST":  # Check if the request method is POST
        username = request.form.get("username")  # Get the username from the form data
        oldPassword = request.form.get("oldPassword")  # Get the old password from the form data
        newPassword = request.form.get("newPassword")  # Get the new password from the form data
        confirmation = request.form.get("confirmation")  # Get the password confirmation from the form data

        # Query database for user
        table = db.execute("SELECT * from users WHERE username = :username", username=username)  # Retrieve user data from the database
        oldPasswordHash = table[0]["hash"] if table else None  # Get the hashed old password from the database

        # Validate old password, new password, and confirmation
        if not oldPasswordHash or not check_password_hash(oldPasswordHash, oldPassword) or newPassword != confirmation:
            return apology("Invalid password change", 400)  # Return an apology if the password change is invalid

        # Validate new password complexity
        if not re.search("[!@#$%^&*()]", newPassword) or not re.search("[0-9]", newPassword) or len(newPassword) <= 5:
            return apology("Password must meet complexity requirements", 400)  # Return an apology if the new password doesn't meet complexity requirements

        # Update user's password hash
        newHash = generate_password_hash(newPassword)  # Generate a new hash for the new password
        db.execute("UPDATE users SET hash = :newHash WHERE username = :username", newHash=newHash, username=username)  # Update the user's password hash in the database

        return redirect("/login")  # Redirect the user to the login page after successfully changing the password
    else:
        return render_template("changePassword.html")  # Render the changePassword.html template for displaying the change password form

# User registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()  # Clear any existing session data

    if request.method == "POST":  # Check if the request method is POST
        username = request.form.get("username")  # Get the username from the form data
        password = request.form.get("password")  # Get the password from the form data
        confirmation = request.form.get("confirmation")  # Get the password confirmation from the form data

        # Validate username, password, and confirmation
        if not username or not password or not confirmation or password != confirmation:
            return apology("Invalid registration form", 400)  # Return an apology if the registration form is invalid

        # Check if username already exists
        if db.execute("SELECT * FROM users WHERE username = :username", username=username):
            return apology("Username already exists", 400)  # Return an apology if the username already exists in the database

        # Validate password complexity
        if not re.search("[!@#$%^&*()]", password) or not re.search("[0-9]", password) or len(password) <= 5:
            return apology("Password must meet complexity requirements", 400)  # Return an apology if the password doesn't meet complexity requirements

        # Insert new user into database
        hash = generate_password_hash(password)  # Generate a hash for the password
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)  # Insert the new user into the database

        # Log in the newly registered user
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)  # Retrieve the newly registered user's data
        session["user_id"] = rows[0]["id"]  # Set the user_id in the session

        return redirect("/login")  # Redirect the user to the login page after successful registration
    else:
        return render_template("register.html")  # Render the register.html template for displaying the registration form

# Sell stocks route
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session.get("user_id")  # Get the user ID from the session
    if user_id is None:  # Check if the user ID is not found in the session
        return apology("User ID not found in session", 400)  # Return an apology if user ID is not found

    if request.method == "POST":  # Check if the request method is POST
        symbol = request.form.get("symbol")  # Get the symbol from the form data
        shares_str = request.form.get("shares")  # Get the number of shares from the form data

        if not symbol or not shares_str:  # Check if both symbol and shares are provided
            return apology("Please provide both symbol and shares", 400)  # Return an apology if symbol or shares are missing

        try:
            shares = int(shares_str)  # Convert shares_str to an integer
            if shares <= 0:
                return apology("Shares must be a positive integer", 400)  # Return an apology if shares are not a positive integer
        except ValueError:
            return apology("Shares must be a valid number", 400)  # Return an apology if shares are not a valid number

        # Retrieve user's stocks for the given symbol
        user_stocks = db.execute("SELECT * FROM purchases WHERE user_id = :user_id AND symbol = :symbol", user_id=user_id, symbol=symbol)
        if not user_stocks:  # Check if the user does not own any shares of the symbol
            return apology(f"User {user_id} does not own any shares of {symbol}", 400)  # Return an apology if user does not own shares of the symbol
        print("user_stocks")

        total_shares = sum(stock["shares"] for stock in user_stocks)  # Calculate the total shares owned by the user
        if total_shares < shares:  # Check if the user does not have enough shares to sell
            return apology("Not enough shares available for selling", 400)  # Return an apology if not enough shares are available

        # Calculate the sell price from the stock quote
        quote = lookup(symbol)  # Get the stock quote for the symbol
        if not quote:  # Check if the quote is not found
            return apology("Symbol not found", 400)  # Return an apology if symbol is not found

        price = quote["price"]  # Get the price from the quote
        total = price * shares  # Calculate the total value of the shares to be sold

        # Record the sale in the 'history' table
        db.execute("INSERT INTO history (user_id, symbol, shares, price, transaction_type, total) VALUES (:user_id, :symbol, :shares, :price, 'Sell', :total)",
                   user_id=user_id, symbol=symbol, shares=shares, price=price, total=total)

        # Update user's cash balance after sale
        db.execute("UPDATE users SET cash = cash + :total WHERE id = :user_id", total=total, user_id=user_id)

        # Update the 'purchases' table to reflect the sold shares
        for stock in user_stocks:
            if stock["shares"] <= shares:  # Check if the current stock has fewer shares than the requested sell shares
                db.execute("DELETE FROM purchases WHERE id = :stock_id", stock_id=stock["id"])  # Delete the stock entry from purchases table
                shares -= stock["shares"]  # Reduce the remaining shares to be sold
            else:
                db.execute("UPDATE purchases SET shares = shares - :shares WHERE id = :stock_id", shares=shares, stock_id=stock["id"])
                break  # Exit the loop after updating the shares
        # Flash success message
        flash("Stock sold successfully!", "success")

        return redirect("/")  # Redirect to the homepage after successful sale
    else:
        stocks = db.execute("SELECT symbol FROM purchases WHERE user_id = :user_id", user_id=user_id)  # Get the symbols of stocks owned by the user
        return render_template("sell.html", stocks=stocks)  # Render the sell.html template with the user's stocks for selling

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
