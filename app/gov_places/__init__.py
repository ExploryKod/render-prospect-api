from flask import Blueprint

gov_places = Blueprint('gov_places', __name__)


from app.gov_places import routes