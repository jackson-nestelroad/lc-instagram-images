import string
import requests
from bs4 import BeautifulSoup

from models import *
from models.db import db


class ScrapeException(Exception):
    pass


life_church = 'https://life.church'
open_life_church = 'https://open.life.church'


def get_media_url():
    full_url = life_church + '/media/messages/'
    page = requests.get(full_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.select('#sermon a')
    if len(links) == 0:
        raise ScrapeException('Could not find latest sermon at ' + full_url)
    return links[0]['href']


def get_resources_url():
    full_url = life_church + get_media_url()
    page = requests.get(full_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.select('.more-resource-tracking >li >a')
    if len(links) == 0:
        raise ScrapeException('Could not find resource links at ' + full_url)

    links = [link for link in links if link.text == 'Church Resources']
    if len(links) == 0:
        raise ScrapeException('Could not find "Church Resources" link at ' + full_url)

    return links[0]['href']


def get_image_url(open_url):
    full_url = open_life_church + open_url
    page = requests.get(full_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    images = soup.select('.item-preview >img')
    if len(images) == 0:
        raise ScrapeException('Could not find image at ' + full_url);
    return images[0]['src']


def generate_message_info_and_resources(resources_url, tag):
    page = requests.get(resources_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    metadata = soup.select_one('.group-meta')
    if metadata is None:
        raise ScrapeException('Could not find message metadata at ' + resources_url);
    try:
        msg_name = MessageName.query.first()
        new_name = metadata.find('h1').text
        if msg_name is None:
            msg_name = MessageName(new_name, resources_url)
            db.session.add(msg_name)
        else:
            msg_name.name = new_name
            msg_name.url = resources_url
        msg_parts = int(metadata.find('p').text.strip(string.ascii_letters))
    except ValueError as e:
        raise ScrapeException(e)

    groups = soup.select('.resource-group')
    if groups is None:
        raise ScrapeException('Could not find any resources at ' + resources_url)

    for part in range(1, msg_parts + 1):
        this_group = [g for g in groups if ('Part %d' % part) in g.find('h3').text]
        if len(this_group) == 0:
            new_error = Error(part, 'Could not find resources for Part %d at %s' % (part, resources_url))
            db.session.add(new_error)
            continue
        images = this_group[0].select('li.resource-item >a.item-title')
        images = [image for image in images if tag in image.text]
        if len(images) == 0:
            new_error = Error(part, 'Could not find resources marked "%s" at %s' % (tag, resources_url))
            db.session.add(new_error)
            continue
        for image in images:
            image_url = get_image_url(image['href'])
            db.session.add(InstagramImage(part, image.text, image_url))
    db.session.commit()