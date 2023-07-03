from flask_sqlalchemy import SQLAlchemy
import datetime
from attr import validate

db = SQLAlchemy()

class Episode(db.Model):
    __tablename__ = 'Episode'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
 
# add any models you may need. 
    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan')


class Appearance(db.Model):
    __tablename__ = 'appearance'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validate('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5 (inclusive).")
        return rating