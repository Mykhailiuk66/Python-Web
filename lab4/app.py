from flask import Flask, render_template, request, redirect, flash, url_for, session, render_template_string
from form import Myform
from datetime import datetime
import os
import random
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty'

logging.basicConfig(filename='app.log', encoding='UTF-8', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


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
    return render_template('projects.html', projects=projects)



@app.route('/about')
def about():
    checker = random.randint(1, 3)

    return render_template('about.html', checker=checker)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = Myform()
    
    if form.validate_on_submit():
        session['username'] = form.name.data
        session['email'] = form.email.data
        
        form.name.data = ''
        form.email.data = ''
        
        flash("Data sent successfully: " + session['username']+ ' ' + session['email'], category = 'success')
        logging.info("Data sent successfully: " + session['username']+ ' ' + session['email'])
        
        return redirect(url_for("contact"))
    
    elif request.method == 'POST':
        flash("Not correct data", category = 'warning')
        logging.warning("Not correct data")
        
    
    if session.get('email'):
        form.name.data = session.get('username')
        form.email.data = session.get('email')

    return render_template('contact.html', form=form)
 
 
@app.route('/delete_session')
def delete_session():
    session.pop('email', default=None)
    session.pop('username', default=None)
    return  render_template('delete_page.html')
   

if __name__ == "__main__":
    app.run()