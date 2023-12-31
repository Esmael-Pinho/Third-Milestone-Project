from datetime import datetime
from flask import flash, render_template, request, redirect, session, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from coreshare import app, db
from coreshare.model import User, Category, Post
from sqlalchemy.exc import SQLAlchemyError
import requests
from requests.exceptions import MissingSchema, ConnectionError


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

        # Check if the user provided an image URL
        if not category_image_url:
            # If not, set a default image URL
            category_image_url = "https://t4.ftcdn.net/jpg/04/00/24/31/360_F_400243185_BOxON3h9avMUX10RsDkt3pJ8iQx72kS3.jpg"

        try:
            # Validate image URL
            if not is_valid_image_url(category_image_url):
                raise MissingSchema("Invalid image URL")

            # Get the user_id of the currently logged-in user
            user_id = User.query.filter_by(user_name=session["user"]).first().id

            new_category = Category(
                category_name=category_name,
                category_image_url=category_image_url,
                user_id=user_id  # Associate the category with the current user
            )

            db.session.add(new_category)
            db.session.commit()

            flash("Category added successfully!", category="success")
            return redirect(url_for("categories"))

        except (MissingSchema, ConnectionError, Exception) as e:
            flash("Invalid image URL, please try again", category="error")
            return render_template("add_category.html")

    return render_template("add_category.html")


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        category.category_image_url = request.form.get("category_image_url")
        db.session.commit()

        flash("Category edited successfully!", category="success")
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    # Check if the current user is the owner of the category
    if category.owner.user_name != session["user"]:
        flash("You don't have permission to delete this category.", category="error")
        return redirect(url_for("categories"))

    # Check if there are posts in the category created by other users
    other_user_posts = Post.query.filter(Post.category_id == category.id, Post.author != category.owner).count()
    if other_user_posts > 0:
        flash("Cannot delete category while there's posts from other users on it.", category="error")
        return redirect(url_for("categories"))

    # If all checks pass, delete the category
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted successfully!", category="success")
    return redirect(url_for("categories"))


@app.route("/posts")
def posts():
    if "user" in session:
        user = User.query.filter_by(user_name=session["user"]).first()
    else:
        # Handle the case when 'user' is not in the session
        flash("User not found in session. Please log in.", category="error")
        return redirect(url_for("login"))


    if user:
        # Fetch posts associated with the logged-in user
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at).all()
        categories = Category.query.order_by(Category.created_at).all()
        return render_template("posts.html", posts=posts, categories=categories)
    else:
        flash("User not found", category="error")
        return redirect(url_for("login"))




@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    categories = list(Category.query.order_by(Category.category_name).all())

    if request.method == 'POST':
        post_name = request.form.get("post_name")
        post_description = request.form.get("post_description")
        post_image_url = request.form.get("post_image_url")

        # Check if the user provided an image URL
        if not post_image_url:
            # If not, set a default image URL
            post_image_url = "https://t4.ftcdn.net/jpg/04/00/24/31/360_F_400243185_BOxON3h9avMUX10RsDkt3pJ8iQx72kS3.jpg"

        # Check if a category is selected
        category_id = request.form.get("category_id")
        if category_id is None or category_id == "Choose Category":
            flash("Please select a category before submitting the form.", category="error")
            return render_template('add_post.html', categories=categories)

        try:
            # Validate image URL if provided
            if post_image_url and not is_valid_image_url(post_image_url):
                raise MissingSchema("Invalid image URL")

            # Get the user_id of the currently logged-in user
            user_id = User.query.filter_by(user_name=session["user"]).first().id

            created_at = datetime.utcnow()
            is_new = bool(request.form.get("is_new"))

            new_post = Post(
                post_name=post_name,
                post_description=post_description,
                created_at=created_at,
                post_image_url=post_image_url,
                is_new=is_new,
                user_id=user_id, 
                category_id=category_id
            )

            db.session.add(new_post)
            db.session.commit()

            flash("Your post has been created!", category="success")
            return redirect(url_for('posts'))

        except (MissingSchema, ConnectionError, Exception) as e:
            flash("Not an image URL, please try again and make sure to include the full image address", category="error")
            return render_template('add_post.html', categories=categories)

    return render_template('add_post.html', categories=categories)



@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if 'user' not in session:
        # User is not logged in, redirect to login page
        flash("User not found in session. Please log in.", category="error")
        return redirect(url_for('login'))

    post = Post.query.get_or_404(post_id)
    categories = list(Category.query.order_by(Category.category_name).all())

    # Ensure the logged-in user is the owner of the post
    if post.author.user_name != session["user"]:
        flash("You don't have permission to edit this post.", category="error")
        return redirect(url_for("posts"))

    if request.method == "POST":
        post.post_name = request.form.get("post_name")
        post.post_description = request.form.get("post_description")
        post.is_new = bool(True if request.form.get("is_new") else False)
        post.category_id = request.form.get("category_id")
        db.session.commit()

        flash("Post edited successfully!", category="success")
        return redirect(url_for("posts"))
    return render_template("edit_post.html", post=post, categories=categories)


def is_valid_image_url(url):
    if not url:
        
        return True
    
    response = requests.get(url)
    return response.status_code == 200 and response.headers['Content-Type'].startswith('image')



@app.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Ensure the logged-in user is the owner of the post
    if post.author.user_name != session["user"]:
        flash("You don't have permission to edit this post.", category="error")
        return redirect(url_for("posts"))
    
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("posts"))
