from datetime import datetime

from .db import db


class Error(db.Model):
    __tablename__ = 'errors'

    id = db.Column(db.Integer, primary_key=True)
    part = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String())
    timestamp = db.Column(db.DateTime(timezone=False), nullable=False)

    def __init__(self, part, message):
        self.part = part
        self.message = message
        self.timestamp = datetime.now()