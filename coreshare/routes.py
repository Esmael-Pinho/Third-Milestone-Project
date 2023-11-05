import datetime
from flask import flash, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from coreshare import app, db
from coreshare.model import User


@app.route("/")
def home():
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
        return redirect(url_for(""))

    return render_template("register.html")


