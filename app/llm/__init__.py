from flask import Blueprint

llm = Blueprint('llm', __name__)

from app.llm import routes 