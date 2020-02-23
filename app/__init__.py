import markdown

from flask import Flask, request
from flask_moment import Moment
from flask_babel import Babel

from config import Config


app = Flask(__name__)
moment = Moment(app)
babel = Babel(app)
md = markdown.Markdown(extensions=['extra', 'toc', 'meta', 'markdown_katex',
                                   'plantuml_markdown'])


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


app.config.from_object(Config)

from app import routes, queries, errors
