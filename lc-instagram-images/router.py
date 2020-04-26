from flask import render_template
from models import *
from models.db import db

from app import app


@app.route('/')
def get_index():
    parts = db.session.query(db.func.max(InstagramImage.part)).scalar()
    message = MessageName.query.first()
    if parts is None:
        errors = Error.query.filter(Error.part < 0).all()
        return render_template('error.html', errors=errors)
    return render_template('index.html', message=message, range=range(1, parts + 1))


@app.route('/<int:part>')
def get_instagram_images(part):
    images = InstagramImage.query.filter_by(part=part).all()
    if len(images) == 0:
        errors = Error.query.filter((Error.part == part) | (Error.part < 0)).all()
        return render_template('error.html', errors=errors)
    return render_template('images.html', images=images)
