import datetime
from flask import flash, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from coreshare import app, db
from coreshare.model import User, Post
import requests


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
                "Username already exists. Please try a different username", category="error")
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
        flash("Registration Successful!", category="success")
        return redirect(url_for("index"))

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
                return redirect(url_for("index"))
            else:
                # not password match
                flash("Incorrect Password, please try again.", category="error")

        else:
            # username doesn't exist
            flash("Username doesn't exist, try register first.", category="error")
            return redirect(url_for("register"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """remove users from session """
    flash("You have been logged out.", category="success")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/contact")
def contact():
    return render_template("contact.html")



@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/profile")
def profile():
    profile = list(Post.query.order_by(Post.post_name).all())
    return render_template("profile.html", profile=profile)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        post_name = request.form.get("post_name")
        post_description = request.form.get("post_description")
        image_url = request.form.get("image_url")
        
        
        # Validate image URL
        response = requests.get(image_url)
        if response.status_code == 200 and response.headers['Content-Type'].startswith('image'):
            user_id = session.get("user_id")

            # Get the current timestamp
            created_at = datetime.utcnow()

            post = Post(
                post_name=post_name,
                post_description=post_description,
                created_at=created_at,
                image_url=image_url,
                user_id=user_id
            )

            db.session.add(post)
            db.session.commit()

            flash("Your post has been created!", category="success")
            return redirect(url_for('index'))
        else:
            return render_template('add_post.html', error='Invalid image URL')

    else:
        return render_template('add_post.html')


@app.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("profile"))


