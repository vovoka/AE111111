from flask import render_template
from app import app
from http.client import HTTPException

@app.errorhandler(404)
def not_found_error(e):
    return render_template('errors/404.html', e=e), 404


@app.errorhandler(Exception)
def internal_error(e):
    if isinstance(e, HTTPException):
        return e
    return render_template("errors/500.html", e=e), 500
