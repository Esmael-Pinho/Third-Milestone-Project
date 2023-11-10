from coreshare import db


class User(db.Model):
    # User model
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    user_first_name = db.Column(db.String(80), nullable=False)
    user_last_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(260), nullable=False)
    posts = db.relationship("Post")
    notes = db.relationship("Notes")
    events = db.relationship("Events")

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Username: {1} | First name: {2}".format(
            self.id, self.user_name, self.user_first_name
        )


class Post(db.Model):
    # schema for the Posts model
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(35), unique=True, nullable=False)
    events = db.relationship("Events")
    post_description = db.Column(db.Text, nullable=False)
    post_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.post_name


class Notes(db.Model):
    # schema for the Notes model
    id = db.Column(db.Integer, primary_key=True)
    notes_name = db.Column(db.String(50), unique=True, nullable=False)
    notes_description = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Notes: {1} | Urgent: {2}".format(
            self.id, self.notes_name, self.is_urgent
        )


class Events(db.Model):
    # schema for the Notes model
    id = db.Column(db.Integer, primary_key=True)
    events_name = db.Column(db.String(50), unique=True, nullable=False)
    events_description = db.Column(db.Text, nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Events: {1} | Date: {2}".format(
            self.id, self.events_name, self.from_date
        )