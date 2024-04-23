import os
from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


db = SQL("sqlite:///project.db")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    # clear session
    session.clear()
    # check if username is given
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        rows = db.execute("SELECT * FROM users WHERE username == ?", username)
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return render_template("register.html", text = "Please create an account!")
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/genres")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        accounts = db.execute("SELECT * FROM users WHERE username == ?", name)
        hash = generate_password_hash(password)
        if password != confirmation:
            session["error"] = True
            return render_template("register.html", text = "Sorry, your passwords do not match!")
        if len(accounts) != 0:
            session["error"] = True
            return render_template("register.html", text = "Sorry, account already exists!")
        db.execute("INSERT INTO users (username, password) VALUES (?,?)", name, hash)
        return redirect("/login")
    if request.method == "GET":
        return render_template("register.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session.get("user_id")
    data = db.execute("SELECT * FROM users WHERE id == ?", user_id)
    return render_template("profile.html",data = data )

@app.route("/about", methods=["GET", "POST"])
@login_required
def about():
    return render_template("about.html")

@app.route("/genres", methods=["GET", "POST"])
@login_required
def genres():
    if request.method == "POST":
        GENRES = db.execute("SELECT * FROM genres")
        select = request.form.get("select")
        rows = db.execute("SELECT DENSE_RANK() OVER(ORDER BY votes DESC) AS rank,name,votes FROM votes WHERE genre == ?", select)
        if not select:
            session["error"] = True
            return render_template("genres.html",GENRES = GENRES, text = "Sorry, please choose a poll")
        session["genre"] = select
        return render_template("home.html", rows = rows, title = select)
    else:
        GENRES = db.execute("SELECT DISTINCT * FROM genres")
        return render_template("genres.html", GENRES = GENRES)

@app.route("/vote", methods=["GET", "POST"])
@login_required
def vote():
    if request.method == "POST":
        name = request.form.get("name")
        select = session.get("genre")
        db.execute("UPDATE votes SET votes = (votes + 1) WHERE name == ?", name)
        rows = db.execute("SELECT DENSE_RANK() OVER(ORDER BY votes DESC) AS rank,name,votes,genre FROM votes WHERE genre == ?", select)
        return render_template("home.html", rows = rows, title = select)
    else:
        return render_template("genre.html")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method=="POST":
        name = request.form.get("poll_name")
        GENRES = db.execute("SELECT * FROM genres WHERE genres == ?",name)
        if len(GENRES) != 0:
            session["error"] = True
            return render_template("create.html", text = "Sorry, Poll already exists!")
        else:
            db.execute("INSERT INTO genres(genres) VALUES(?)",name)
            session["genre"] = name
            table = db.execute("SELECT DENSE_RANK() OVER(ORDER BY votes DESC) AS rank,name,votes FROM votes WHERE genre == ?", name)
            return render_template("home.html", rows=table, title = name)
    else:
        return render_template("create.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method=="POST":
        name =request.form.get("option")
        genre = session.get("genre")
        db.execute("INSERT INTO votes(genre, name, votes) VALUES(?,?,?)", genre, name, 0)
        table = db.execute("SELECT DENSE_RANK() OVER(ORDER BY votes DESC) AS rank,name,votes FROM votes WHERE genre == ?", genre)
        return render_template("home.html", rows=table, title = genre)
    else:
        genre = request.args.get("genre")
        session["genre"] = genre
        return render_template("add.html")

@app.route("/chuser", methods=["GET", "POST"])
@login_required
def chuser():
    if request.method=="POST":
        username=request.form.get("username")
        user_id = session.get("user_id")
        db.execute("UPDATE users SET username = ? WHERE id == ?", username, user_id)
        return redirect("/profile")
    else:
        return render_template("profile.html")

@app.route("/chpassword", methods=["GET", "POST"])
@login_required
def chpass():
    if request.method == "POST":
        user_id = session.get("user_id")
        pw = db.execute("SELECT password FROM users WHERE id == ?", user_id)
        old = request.form.get("password")
        new = request.form.get("password2")
        confirm = request.form.get("confirmation")
        pw1 = pw[0]["password"]
        if check_password_hash(pw1, request.form.get("password")) != True:
            session["password"] = True
            return render_template("profile.html", text = "Sorry, Incorrect password!")
        elif new != confirm:
            session["password"] = True
            return render_template("profile.html", text = "Sorry, passwords do not match!")
        else:
            db.execute("UPDATE users SET password = ? WHERE id == ?", generate_password_hash(new), user_id)
            return redirect("/profile")
    else:
        return render_template("profile.html")
