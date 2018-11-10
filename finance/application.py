import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    id = session["user_id"]

    # Select user's cash balance
    cash = db.execute("SELECT cash FROM users where id=:id", id=id)
    avail_cash = cash[0]["cash"]

    # Collect users portfolio info
    update_stocks = db.execute("SELECT * FROM portfolios WHERE id=:id", id=id)

    # Intialize grand total calculation
    grand_total=avail_cash

    # Loop through each stock in portfolio to update share price and total
    for stock in update_stocks:
        updates = lookup(stock["Symbol"])
        price_update = updates["price"]
        shares = stock["Shares"]
        total_update = price_update*shares
        db.execute("UPDATE portfolios SET Price=:price_update, Total=:total_update WHERE id=:id AND Symbol=:symbol", id=id, symbol=stock["Symbol"], price_update=usd(price_update), total_update=usd(total_update))
        grand_total+=total_update

    stocks = db.execute("SELECT * FROM portfolios WHERE id=:id", id=id)

    # Render home page
    return render_template("home.html", stocks=stocks, avail_cash=usd(avail_cash), grand_total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Lookup stock
        buyvals=lookup(request.form.get("symbol"))
        shares=request.form.get("shares")

        # Remember user's session
        id=session["user_id"]

        # Validate order inputs
        if buyvals == None:
            return apology("Invalid stock symbol")
        elif not shares:
            return apology("must enter postive number of shares")
        elif int(shares)<1:
            return apology("shares must be a postive integer")

        # Stock info
        symbol=buyvals["symbol"]
        name=buyvals["name"]
        share_price = buyvals["price"]
        total_price = int(shares)*float(share_price)

        # Check user's available cash
        cash=db.execute("SELECT cash FROM users WHERE id=:id", id=id)
        avail_cash=float(cash[0]["cash"])

        # return render_template("test.html", id=id,price=share_price,total_price=total_price, avail_cash=avail_cash)

        #Check if user has sufficient cash for purchase
        if avail_cash>=total_price:

            # Log purchase in transactions table
            db.execute("INSERT INTO transactions (id, Symbol, Shares, Price, Total, Action) VALUES (:id, :symbol, :shares, :share_price, :total_price, :action)", id=id, symbol=symbol, shares=shares, share_price=usd(share_price), total_price=usd(total_price), action="Buy")

            # Check if user already owns some of the same stock
            if not db.execute("SELECT shares FROM portfolios WHERE id=:id AND Symbol=:symbol", id=id, symbol=symbol):
                # Insert stocks into portfolio if user does not already own some
                db.execute("INSERT INTO portfolios (id, Company, Symbol, Shares, Price, Total) VALUES (:id, :name, :symbol, :shares, :share_price, :total_value)", id=id, name=name, symbol=symbol, shares=shares, share_price=share_price, total_value=total_price)

            # Update portfolio if user already owns shares
            else:

                # Previus number of shares
                prev_info=db.execute("SELECT * FROM portfolios WHERE id=:id AND Symbol=:symbol", id=id, symbol=symbol)
                prev_shares=int(prev_info[0]["Shares"])

                # Updated shares & total value
                nshares=int(shares)+prev_shares
                total_value=nshares*share_price

                # Update user's portfolio
                db.execute("UPDATE portfolios SET Shares=:nshares, Price=:share_price, Total=:ntotal_value WHERE id=:id AND Symbol=:symbol",id=id, symbol=symbol, nshares=nshares, share_price=share_price, ntotal_value=total_value)

            # Update user's available cash
            db.execute("UPDATE users SET cash=:ncash WHERE id=:id", id=id, ncash=avail_cash-total_price)

            # return render_template("bought.html", id=id, name=name, symbol=symbol, shares=shares, price=share_price, total_price=total_price)
            return redirect("/")


        # Return apology if insufficient cash
        else:
            return apology("Sorry, you do not have sufficient funds")
    # # User reached route via GET (clicked on buy link)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    id=session["user_id"]
    transactions = db.execute("SELECT * FROM transactions WHERE id=:id", id=id)
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Lookup name and price of stock using symbol
        quote=lookup(request.form.get("symbol"))
        # If stock symbol does not exist, return apology
        if quote==None:
            return apology("Invalid stock symbol")
        # If stock symbol does exist, render quoted.html to display values
        else:
            return render_template("quoted.html", name=quote["name"], price=usd(quote["price"]), symbol=quote["symbol"])

    # Render quote.html if user clicks on quote link
    else:
        return render_template("quote.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add cash"""
    if request.method =="POST":
        if not request.form.get("add"):
            return apology("must enter cash amount")
        elif float(request.form.get("add"))<0:
            return apology("must enter postivive cash amount")
        else:
            id = session["user_id"]

            # Update user's cash amount
            cash_request=db.execute("SELECT cash FROM users WHERE id=:id", id=id)
            current_cash = float(cash_request[0]["cash"])
            add_cash = float(request.form.get("add"))
            updated_cash = current_cash+add_cash
            db.execute("UPDATE users SET cash=:cash WHERE id=:id", id=id, cash=updated_cash)

            # Log cash addition in transactions
            db.execute("INSERT INTO transactions (id, Symbol, Shares, Price, Total, Action) VALUES (:id, :symbol, :shares, :share_price, :total_price, :action)", id=id, symbol="Cash", shares="N/A", share_price="N/A", total_price=usd(add_cash), action="Add")

            return redirect("/")
    else:
        return render_template("add.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password and confirmation match
        elif request.form.get("password")!=request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        else:
            # Check if username exists
            rows = db.execute("SELECT username FROM users WHERE username=:username", username=request.form.get("username"))
            if len(rows)==1:
                # Return apology if username already exists
                return apology("username already exists", 403)
            else:
                # Hash password
                hash=generate_password_hash(request.form.get("password"))

                # Insert new username and password into users database
                db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=hash)

                # Remember session
                result=db.execute("SELECT * FROM users WHERE username=:username", username=request.form.get("username"))
                session["user_id"] = result[0]["id"]


                # Login and redirect to homepage
                return redirect("/")

    # User reached route via GET (ie. Clicking register link)
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        # Check user's inputs
        if not request.form.get("symbol"):
            return apology("must select a valid stock")
        elif int(request.form.get("shares"))<1:
            return apology("must enter a postive number of shares")
        else:
            # Store session id
            id=session["user_id"]

            # Look up share price on stock to sell
            symbol = request.form.get("symbol")
            sell_info = lookup(symbol)

            # Calculate new total value
            portfolio_shares = db.execute("SELECT Shares FROM portfolios WHERE id=:id AND Symbol=:symbol", id=id, symbol=symbol)
            existing_shares = int(portfolio_shares[0]["Shares"])
            updated_shares = existing_shares-int(request.form.get("shares"))

            # Make sure user has enough shares to make the sale
            if updated_shares<0:
                return apology("you do not have enough shares")
            # Delete stock from portfolio if user is selling all existing shares
            elif updated_shares == 0:
                db.execute("DELETE FROM portfolios WHERE id=:id AND Symbol=:symbol", id=id, symbol=symbol)
            # Otherwise update the shares, share price, and total for the stock in the portfolio
            else:
                updated_total = updated_shares*sell_info["price"]
                db.execute("UPDATE portfolios SET Shares=:shares, Price=:price, Total=:total WHERE id=:id AND Symbol=:symbol", shares=updated_shares, price=sell_info["price"], total=updated_total, id=id, symbol=symbol)

            # Update user's cash
            cash_added = int(request.form.get("shares"))*sell_info["price"]
            cash_info = db.execute("SELECT cash FROM users WHERE id=:id", id=id)
            updated_cash = cash_added+cash_info[0]["cash"]
            db.execute("UPDATE users SET cash=:cash WHERE id=:id", id=id, cash=updated_cash)

            # Insert transaction info into transaction table
            db.execute("INSERT INTO transactions (id, Symbol, Shares, Price, Total, Action) VALUES (:id, :symbol, :shares, :share_price, :total_price, :action)", id=id, symbol=symbol, shares=request.form.get("shares"), share_price=usd(sell_info["price"]), total_price=usd(cash_added), action="Sell")
            return redirect("/")
    else:
        sell_stocks = db.execute("SELECT * FROM portfolios WHERE id=:id", id=session["user_id"])
        return render_template("sell.html", sell_stocks=sell_stocks)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
