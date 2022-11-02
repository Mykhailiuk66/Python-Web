from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
import random

app = Flask(__name__)


projects = [
    {
        'id': 1,
        'title': "COCOMO",
        'description': "The Constructive Cost Model (COCOMO) is a procedural software cost estimation model developed by Barry W. Boehm. The model parameters are derived from fitting a regression formula using data from historical projects (63 projects for COCOMO 81 and 163 projects for COCOMO II).",
    },
    {
        'id': 2,
        'title': "COCOMO 2",
        'description': "COCOMO-II is the revised version of the original Cocomo (Constructive Cost Model) and is developed at University of Southern California. It is the model that allows one to estimate the cost, effort and schedule when planning a new software development activity.",
    },
    {
        'id': 3,
        'title': "Cube 3D",
        'description': "Cube3d is a three-dimensional solid object bounded by six square faces, facets or sides, with three meeting at each vertex.",
    },
    {
        'id': 4,
        'title': "In progress",
        'description': "In progress...",
    },
    
]



@app.route('/')
def index():
    info = {
        'os_name': os.name,
        'user_agent': request.headers.get('User-Agent'),
        'current_time': datetime.now().strftime("%H:%M:%S")
    }
    
    return render_template('index.html', projects=projects, info=info)



@app.route('/about')
def about():
    info = {
        'os_name': os.name,
        'user_agent': request.headers.get('User-Agent'),
        'current_time': datetime.now().strftime("%H:%M:%S")
    }
    
    checker = random.randint(1, 3)

    return render_template('about.html', info=info, checker=checker)


@app.route('/redirect-example')
def redirect_example():
    return redirect('contact')


@app.route('/contact')
def contact():
    info = {
        'os_name': os.name,
        'user_agent': request.headers.get('User-Agent'),
        'current_time': datetime.now().strftime("%H:%M:%S")
    }

    
    return render_template('contact.html', info=info)


if __name__=="__main__":
    app.run()