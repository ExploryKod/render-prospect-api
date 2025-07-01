from flask import Blueprint

google_places = Blueprint('google_places', __name__)


from app.google_places import routes