from flask import Flask, render_template

import scraper

app = Flask(__name__)


@app.route('/')
def get_index():
    return render_template('index.html', range=range(1, 5))


@app.route('/<int:part>')
def get_instagram_images(part):
    try:
        images = scraper.get_open_urls('Instagram', part)
        images = list(map(lambda url: scraper.get_image_url(url), images))
    except scraper.ScrapeException as e:
        return str(e)

    return render_template('images.html', images=images)
