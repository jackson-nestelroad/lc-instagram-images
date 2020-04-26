from .db import db


class MessageName(db.Model):
    __tablename__ = 'message_name'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    url = db.Column(db.String())

    def __init__(self, name, url):
        self.name = name
        self.url = url
