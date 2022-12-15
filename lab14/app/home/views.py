import random
from flask import render_template
from . import home_bp
from .data import projects


@home_bp.route('/')
def index():
    return render_template('home/projects.html', projects=projects)


@home_bp.route('/about')
def about():
    checker = random.randint(1, 3)
    
    return render_template('home/about.html', checker=checker)

