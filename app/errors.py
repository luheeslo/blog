import werkzeug

from flask import render_template

from app import app


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(FileNotFoundError)
def handle_file_not_found(e):
    return render_template("404.html"), 404


app.register_error_handler(404, handle_not_found)
app.register_error_handler(404, handle_file_not_found)
