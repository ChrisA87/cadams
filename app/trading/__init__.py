from flask import Blueprint
from .strategy import SMA, MeanReversion, OLS, Momentum

trading = Blueprint("trading", __name__)

from . import views
