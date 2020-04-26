import os
from flask_migrate import Migrate

from flask import Flask
from models import *
from models.db import db
from scraper.index import scraperbp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(scraperbp)

db.init_app(app)
migrate = Migrate(app, db)