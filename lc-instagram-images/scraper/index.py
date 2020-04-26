from flask import Blueprint

from scraper import *
from models import *
from models.db import db


scraperbp = Blueprint('scraper', __name__)


@scraperbp.cli.command('scrape')
def scrape():
    """ Updates the database with web scraping """
    try:
        InstagramImage.query.delete()
        Error.query.delete()
        resources_url = get_resources_url()
        generate_message_info_and_resources(resources_url, 'Instagram')
    except ScrapeException as e:
        new_error = Error(-1, str(e))
        db.session.add(new_error)
        db.session.commit()
