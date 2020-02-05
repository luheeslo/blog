from app import app
from app.queries import get_recent_articles


@app.shell_context_processor
def make_shell_context():
    return {'get_recent_articles': get_recent_articles}
