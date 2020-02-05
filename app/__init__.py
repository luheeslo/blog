import markdown

from flask import Flask

from config import Config


app = Flask(__name__)
md = markdown.Markdown(extensions=['extra', 'toc', 'meta', 'markdown_katex',
                                   'plantuml_markdown'])

app.config.from_object(Config)

from app import routes, queries, errors
