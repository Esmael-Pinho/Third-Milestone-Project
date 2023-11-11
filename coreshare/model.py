from coreshare import db
from datetime import datetime


class User(db.Model):
    # User model
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    user_first_name = db.Column(db.String(80), nullable=False)
    user_last_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(260), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Username: {1} | First name: {2}".format(
            self.id, self.user_name, self.user_first_name
        )


class Post(db.Model):
    # schema for the Posts model
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(80), nullable=False)
    post_description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user_posts', lazy=True))

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Post: {1} | Description: {2} | Image: {3}".format(
            self.id, self.post_name, self.post_description, self.image_url
        )



