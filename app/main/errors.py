from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(err):
    return render_template('404.html'), 404