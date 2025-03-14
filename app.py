import os
import psycopg2
from datetime import datetime
from pytz import timezone, utc
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Get database URL from environment variables
db_url = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(db_url)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM portfolio WHERE user_id = %s", (user_id,))
    portfolio = cur.fetchall()
    
    cur.execute("SELECT username, cash FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    username = user_data[0]
    user_cash = user_data[1]
    
    cur.close()
    conn.close()
    
    return render_template("index.html", portfolio=portfolio, username=username, cash=user_cash, message="")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    user_id = session["user_id"]
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT cash FROM users WHERE id = %s", (user_id,))
    user_cash = cur.fetchone()[0]
    
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_input = request.form.get("shares")
        
        if not symbol or not lookup(symbol):
            return apology("Invalid stock symbol")

        if not shares_input or not shares_input.isdigit():
            return apology("Number of shares must be positive")
        
        shares = int(shares_input)
        if shares < 1:
            return apology("Shares must be a positive integer.")
        
        stockinfo = lookup(symbol)
        stock_price = stockinfo["price"]
        total_price = shares * stock_price
        
        if user_cash >= total_price:
            cur.execute("UPDATE users SET cash = cash - %s WHERE id = %s", (total_price, user_id))
            cur.execute("INSERT INTO transactions (user_id, symbol, shares, price, total_price, type) VALUES (%s, %s, %s, %s, %s, %s)",
                        (user_id, symbol.upper(), shares, stock_price, total_price, "BUY"))
            cur.execute("SELECT shares FROM portfolio WHERE user_id = %s AND symbol = %s", (user_id, symbol.upper()))
            existing_portfolio = cur.fetchone()
            
            if existing_portfolio:
                cur_shares = existing_portfolio[0]
                cur.execute("UPDATE portfolio SET shares = %s WHERE user_id = %s AND symbol = %s",
                            (cur_shares + shares, user_id, symbol.upper()))
            else:
                cur.execute("INSERT INTO portfolio (user_id, symbol, company_name, shares) VALUES (%s, %s, %s, %s)",
                            (user_id, symbol.upper(), stockinfo["name"], shares))
            conn.commit()
            cur.close()
            conn.close()
            return redirect("/")
        else:
            return apology("Not enough cash!")
    
    cur.close()
    conn.close()
    return render_template("buy.html", cash=user_cash, usd=usd)

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        if not username or not password or password != confirm_password:
            return apology("Invalid username or password")

        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("INSERT INTO users (username, hash) VALUES (%s, %s) RETURNING id", (username, hashed_password))
            user_id = cur.fetchone()[0]
            conn.commit()
            session["user_id"] = user_id
        except psycopg2.Error:
            cur.close()
            conn.close()
            return apology("Username already exists. Choose a different one.")
        
        cur.close()
        conn.close()
        return redirect("/")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id, hash FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not user or not check_password_hash(user[1], password):
            return apology("Invalid username or password")
        
        session["user_id"] = user[0]
        return redirect("/")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()
