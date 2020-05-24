from app.api import user_api, score_api, qa_api, token_api
from app import app
from flask import Blueprint

bp = Blueprint('api', __name__)