from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about-me')
def about():
    return render_template('main/about.html')
