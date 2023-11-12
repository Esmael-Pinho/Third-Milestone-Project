import datetime
from flask import flash, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from coreshare import app, db
from coreshare.model import User, Category, Post
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
        return redirect(url_for("categories"))

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
                return redirect(url_for("categories"))
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


@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.created_at).all())
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category_name = request.form.get("category_name")
        category_image_url = request.form.get("category_image_url")

        # Validate image URL
        if not is_valid_image_url(category_image_url):
            flash("Invalid image URL, please try again", category="error")
            return render_template("add_category.html")

        new_category = Category(category_name=category_name, category_image_url=category_image_url)

        db.session.add(new_category)
        db.session.commit()

        flash("Category added successfully!", category="success")
        return redirect(url_for("categories"))

    return render_template("add_category.html")



@app.route("/posts")
def posts():
    posts = list(Post.query.order_by(Post.id).all())
    return render_template("posts.html", posts=posts)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    categories = list(Category.query.order_by(Category.category_name).all())

    if request.method == 'POST':
        post_name = request.form.get("post_name")
        post_description = request.form.get("post_description")
        post_image_url = request.form.get("post_image_url")

        # Validate image URL
        if not is_valid_image_url(post_image_url):
            flash("Invalid image URL, please try again", category="error")
            return render_template('add_post.html', categories=categories)

        user_id = session.get("user_id")
        created_at = datetime.utcnow()
        is_new = bool(request.form.get("is_new"))

        new_post = Post(
            post_name=post_name,
            post_description=post_description,
            created_at=created_at,
            post_image_url=post_image_url,
            is_new=is_new,
            user_id=user_id
        )

        db.session.add(new_post)
        db.session.commit()

        flash("Your post has been created!", category="success")
        return redirect(url_for('posts'))

    return render_template('add_post.html', categories=categories)


def is_valid_image_url(url):
    response = requests.get(url)
    return response.status_code == 200 and response.headers['Content-Type'].startswith('image')


@app.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("posts"))


