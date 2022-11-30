from flask import Blueprint, render_template, abort

candidate_bp = Blueprint('candidate', __name__,
                        template_folder='templates/candidate_form')

from . import views