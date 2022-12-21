from flask import Blueprint, render_template, abort

account_bp = Blueprint('account', __name__,
                        template_folder='templates/account')

from . import views