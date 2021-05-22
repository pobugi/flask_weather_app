from flask import Blueprint

bp = Blueprint('main', __name__)

from weather_app.main import routes
