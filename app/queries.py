from datetime import datetime
from os import listdir
from os.path import join

from app import app, md


def get_article_file(filename):
    return open(join(app.config['ARTICLES_DIR'], filename))


def get_article_md(filename):
    return get_article_file(filename).read()


def get_articles_md():
    return (get_article_md(filename) for filename in listdir(app.config['ARTICLES_DIR']))


def convert_to_html(md_content):
    return md.convert(md_content)


def get_article(filename):
    return convert_to_html(get_article_md(filename))


def get_articles():
    return (convert_to_html(md_content) for md_content in get_articles_md())


def get_recent_articles(quantity=-1):
    qto = slice(None) if quantity == -1 else slice(quantity)
    return sorted(
            ({'date': get_article_date(),
              'title': get_article_title(),
              'summary': get_article_summary(),
              'tags': get_article_tags(),
              'path': get_article_path()} for article in get_articles()),
            key=lambda e: e['date'], reverse=True)[qto]


def get_metadata():
    return md.Meta


def get_article_title():
    return get_metadata()['title'][0]


def get_article_summary():
    return get_metadata()['summary'][0]


def get_article_date():
    return datetime.strptime(get_metadata()['date'][0], app.config['DATE_FORMAT'])


def get_article_path():
    return get_metadata()['path'][0]


def get_article_tags():
    return get_metadata()['tags']
