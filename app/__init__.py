from tempfile import tempdir
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

def create_app(config_name='default'):

    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    @app.route('/')
    def index():
        return render_template('base.html')

    @app.route('/test')
    def test():
        return render_template('test.html')
    
    return app