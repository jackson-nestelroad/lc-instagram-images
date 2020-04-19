import requests
from bs4 import BeautifulSoup


class ScrapeException(Exception):
    pass


life_church = 'https://life.church'
open_life_church = 'https://open.life.church'

def get_media_url():
    page = requests.get(life_church + '/media/')
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.select('.media-section--sermon .carousel >li:first-child a')
    if len(links) == 0:
        raise ScrapeException('Could not find latest sermon on media page')
    return links[0]['href']


def get_resources_url():
    page = requests.get(life_church + get_media_url())
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.select('.more-resource-tracking >li >a')
    if len(links) == 0:
        raise ScrapeException('Could not find resource links on sermon page')

    links = [link for link in links if link.text == 'Church Resources']
    if len(links) == 0:
        raise ScrapeException('Could not find "Church Resources" link on sermon page')

    return links[0]['href']


def get_open_urls(tag, part):
    page = requests.get(get_resources_url())
    soup = BeautifulSoup(page.content, 'html.parser')
    groups = soup.select('.resource-group')
    groups = [group for group in groups
              if ('Part %d' % part) in group.find('h3').text]
    if len(groups) == 0:
        raise ScrapeException('Could not find resources for Part %d' % part)
    images = groups[0].select('li.resource-item >a.item-title')
    images = [image for image in images if tag in image.text]
    if len(images) == 0:
        raise ScrapeException('Could not find resources marked "%s"' % tag)
    return list(map(lambda image: image['href'], images))


def get_image_url(open_url):
    page = requests.get(open_life_church + open_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    images = soup.select('.item-preview >img')
    if len(images) == 0:
        raise ScrapeException('Could not find image at ' + open_life_church + open_url);
    return images[0]['src']