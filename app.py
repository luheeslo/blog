import calendar

from datetime import datetime

from os import listdir
from os.path import join

import markdown
import werkzeug

from flask import Flask, render_template
from jinja2 import Markup

app = Flask(__name__)
md = markdown.Markdown(extensions=['extra', 'toc', 'meta', 'markdown_katex',
                                   'plantuml_markdown'])
ARTICLES_DIR = 'articles'
RECENT_ARTICLES_QTO = 5
DATE_FORMAT = '%Y-%d-%m'


# queries
def get_article_file(filename):
    return open(join(ARTICLES_DIR, filename))


def get_article_md(filename):
    return get_article_file(filename).read()


def get_articles_md():
    return (get_article_md(filename) for filename in listdir(ARTICLES_DIR))


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
              'path': get_article_path()} for article in get_articles()),
            key=lambda e: e['date'], reverse=True)[qto]


def get_metadata():
    return md.Meta


def get_article_title():
    return get_metadata()['title'][0]


def get_article_summary():
    return get_metadata()['summary'][0]


def get_article_date():
    return datetime.strptime(get_metadata()['date'][0], DATE_FORMAT)


def get_article_path():
    return get_metadata()['path'][0]


# error handlers
@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(FileNotFoundError)
def handle_file_not_found(e):
    return render_template("404.html"), 404


app.register_error_handler(404, handle_not_found)
app.register_error_handler(404, handle_file_not_found)


# routes
@app.route('/')
def index():
    return render_template('index.html',
                           articles=get_recent_articles(RECENT_ARTICLES_QTO))


@app.route('/a/<entry>')
def page(entry):
    return render_template('article.html',
                           article=Markup(
                               get_article('{0}.md'.format(entry))),
                           date=get_article_date(),
                           title=get_article_title())


@app.route('/archive')
def archive():
    articles_details = {}
    for article in get_recent_articles():
        year, month = article['date'].year, calendar.month_name[article['date'].month]
        articles_by_year = articles_details.get(year)
        if articles_by_year is None:
            articles_details.update({year: {month: [article]}})
        else:
            if articles_by_year.get(month):
                articles_by_year[month].append(article)
            else:
                articles_by_year.update({month: [article]})

    return render_template('archive.html', articles=articles_details,
                                           title="Archive")
