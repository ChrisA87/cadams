import os
from app import create_app, db
from app.models import User
from flask_migrate import Migrate

config_name = os.environ.get('FLASK_ENV') or 'default'
app = create_app(config_name)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)
