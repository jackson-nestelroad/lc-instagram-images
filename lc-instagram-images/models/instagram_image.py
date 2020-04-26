from .db import db


class InstagramImage(db.Model):
    __tablename__ = 'instagram_images'

    id = db.Column(db.Integer, primary_key=True)
    part = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String())
    url = db.Column(db.String())

    def __init__(self, part, name, url):
        self.part = part
        self.name = name
        self.url = url

    def __repr__(self):
        return f"<InstagramImage {self.name}>"