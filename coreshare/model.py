from coreshare import db
from datetime import datetime

# Define the association table for the many-to-many relationship between Post and Category
post_category = db.Table(
    'post_category',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)
# Association Table for Category and User
user_category_association = db.Table(
    'user_category_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

class User(db.Model):
    # User model
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    user_first_name = db.Column(db.String(80), nullable=False)
    user_last_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(260), nullable=False)
    categories = db.relationship('Category', back_populates='owner', lazy=True)

    # Establish a one-to-many relationship between User and Post
    user_posts = db.relationship("Post", back_populates="author", lazy=True)
    # Establish a many-to-many relationship between User and Category
    user_categories = db.relationship("Category", secondary=user_category_association, back_populates="users", lazy=True)

    

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Username: {1} | First name: {2}".format(
            self.id, self.user_name, self.user_first_name
        )



class Category(db.Model):
    # schema for the Category model
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), unique=True, nullable=False)
    category_image_url = db.Column(db.String(1024), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Foreign key to represent ownership
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    owner = db.relationship("User", back_populates="categories")
    
    # Establish a many-to-many relationship between Category and User
    users = db.relationship("User", secondary=user_category_association, back_populates="user_categories", lazy=True)
    # Establish a one-to-many relationship between Category and Post
    posts = db.relationship("Post", back_populates="category", cascade="all, delete", lazy=True)

    def __repr__(self):
        return "Name: {0} | Image: {1} | Created At: {2}".format(
            self.category_name, self.category_image_url, self.created_at
        )



class Post(db.Model):
    # schema for the Posts model
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(80), nullable=False)
    post_description = db.Column(db.Text, nullable=False)
    post_image_url = db.Column(db.String(1024), nullable=False)  
    is_new = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey(
        "category.id", ondelete="CASCADE"), nullable=False)
    # Establish a many-to-one relationship between Post and User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", back_populates="user_posts", lazy=True)

    # Establish a many-to-many relationship between Post and Category
    categories = db.relationship("Category", secondary="post_category", backref=db.backref("posts_relation", lazy=True))

     # Establish a many-to-one relationship between Post and Category
    category = db.relationship("Category", back_populates="posts", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Post: {1} | Description: {2} | Image: {3}".format(
            self.id, self.post_name, self.post_description, self.post_image_url
        )



