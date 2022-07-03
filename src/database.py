from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import backref
from datetime import datetime
import string
import random

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    bookmarks = db.relationship('Bookmark', backref="user")
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self):
        return f'User>>> {self.username}'


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=True)
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def generate_short_characters(self):
        chars = string.digits+string.ascii_letters
        short_chars = "".join(random.choices(chars, k=3))

        isExisting = self.query.filter_by(short_url=short_chars).first()
        if (isExisting):
            self.generate_short_characters()
        else:
            return short_chars

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_characters()

    def __repr__(self):
        return f'Bookmark>>> {self.url}'
