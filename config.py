import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    ARTICLES_DIR = os.getenv('ARTICLES_DIR') or 'articles'
    ARTICLES_PER_PAGE = os.getenv('ARTICLES_PER_PAGE') or 5
    DATE_FORMAT = os.getenv('DATE_FORMAT') or '%Y-%d-%m'
    TWITTER_URL = os.getenv('TWITTER_URL') or '#'
    LINKEDIN_URL = os.getenv('LINKEDIN_URL') or '#'
    GITHUB_URL = os.getenv('GITHUB_URL') or '#'
