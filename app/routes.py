import calendar

from flask import render_template
from jinja2 import Markup

from app import app
from app.queries import (get_recent_articles, get_article, get_article_date,
                     get_article_title)


@app.route('/')
def index():
    return render_template('index.html',
                           articles=get_recent_articles(int(app.config['ARTICLES_PER_PAGE'])))


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

    return render_template('archive.html', articles=articles_details, title="Archive")


@app.route('/tags/')
def tags():
    t = []
    for article in get_recent_articles():
        t += article['tags']

    tags_dict = {}
    for tag in set(t):
        tags_dict.update({tag: t.count(tag)})

    return render_template('tags.html', tags=tags_dict)


@app.route('/tags/<tag>')
def get_articles_by_tag(tag):
    articles = [article for article in get_recent_articles()
                if tag in article['tags']]

    return render_template('index.html', articles=articles)
