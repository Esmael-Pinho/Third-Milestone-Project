import datetime
from flask import flash, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from coreshare import app, db
from coreshare.model import User, Post, Notes, Events


@app.route("/")
def intro():
    return render_template("base.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Renders register page and allows user to register"""
    if request.method == "POST":
        # checks if username already exists
        existing_user = User.query.filter(
            User.user_name == request.form.get("user_name").lower()).all()

        if existing_user:
            flash(
                "Username already exists. Please try a different username")
            return redirect(url_for("register"))

        user = User(
            user_name=request.form.get("user_name").lower(),
            user_first_name=request.form.get("first_name").lower(),
            user_last_name=request.form.get("last_name").lower(),
            password=generate_password_hash(request.form.get("password"))
        )

        # Adds the user to the databsase 
        db.session.add(user)
        db.session.commit()

        # put the new user into 'session' mode / active
        session["user"] = request.form.get("user_name").lower()
        flash("Registration Successful!")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Renders login page and allows user to login"""
    if request.method == "POST":
        # check if username exists in db
        existing_user = User.query.filter(
            User.user_name == request.form.get("user_name").lower()).all()

        if existing_user:
            # ensure the passwords match
            if check_password_hash(
                    existing_user[0].password, request.form.get("password")):
                session["user"] = request.form.get("user_name").lower()
                flash("Welcome, {}".format(
                    request.form.get("user_name")))
                return redirect(url_for(
                    "index"))
            else:
                # not password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Username doesn't exist, please try signing up first")
            return redirect(url_for("register"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """remove users from session """
    flash("You have been logged out.")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/contact")
def contact():
    return render_template("contact.html")



@app.route("/index")
def home():
    return render_template("index.html")