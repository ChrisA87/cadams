from flask import Blueprint
from flask_restx import Api

authorizations = {"apikey": {"type": "apiKey", "in": "header", "name": "X-API-KEY"}}

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(
    app=blueprint,
    title="Cadams APIs",
    description=(
        'Use the public key "974004f8-c594-11ed-976c-86ad6bb37ab4" '
        "to access the public endpoints."
    ),
    authorizations=authorizations,
    security="apikey",
)

from .trading import api as namespace_trading
from .models.trading import api as models_trading
from .wordle import api as namespace_wordle

api.add_namespace(namespace_trading)
api.add_namespace(models_trading)
api.add_namespace(namespace_wordle)
