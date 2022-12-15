from flask import Blueprint

category_bp = Blueprint('category', __name__)

from . import views