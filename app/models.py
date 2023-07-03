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