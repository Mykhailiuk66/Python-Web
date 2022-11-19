from flask import render_template, request, redirect, flash, url_for, session, abort
from flask_login import login_user, current_user, logout_user, login_required
from app.form import Myform, RegistrationForm, LoginForm
from app.models import FormModel, User
from app import app, db
import random
from urllib.parse import urlparse, urljoin


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

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc



@app.route('/')
def index():
    return render_template('projects.html', projects=projects)



@app.route('/about')
def about():
    checker = random.randint(1, 3)

    return render_template('about.html', checker=checker)


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = Myform()
    
    if form.validate_on_submit():
        session['username'] = form.name.data
        session['email'] = form.email.data
        
        form_ = FormModel(name=form.name.data, email=form.email.data,
                  phone=form.phone.data, subject=form.subject.data,
                  message=form.message.data)
        
        
        email_exists = FormModel.query.filter_by(email=form.email.data).first()
        phone_exists = FormModel.query.filter_by(phone=form.phone.data).first()
        
        if not email_exists and not phone_exists: 
            try:
                db.session.add(form_)
            except:
                db.session.rollback()
            else:
                db.session.commit()
            
                flash("Data sent successfully: " + session['username']+ ' ' + session['email'], category = 'success')
                app.logger.info("Data sent successfully: " + session['username']+ ' ' + session['email'])
        else:
            flash("User already exists", category="warning")
              
        return redirect(url_for("form"))
    
    elif request.method == 'POST':
        flash("Not correct data", category = 'warning')
        app.logger.warning("Not correct data")
        
        
    
    # if session.get('email'):
    form.name.data = session.get('username')
    form.email.data = session.get('email')

    return render_template('form.html', form=form)
 
 
@app.route('/db_form_table')
def db_form_table():
    forms = FormModel.query.all()
    return  render_template('db_form_table.html', forms=forms)
   

@app.route('/delete_session')
def delete_session():
    session.pop('email', default=None)
    session.pop('username', default=None)
    return  render_template('delete_page.html')
   

@app.route('/delete_object/<int:id>', methods=['GET'])
def delete_object(id):
    # FormModel.query.filter_by(id=id).delete()
    form_model = FormModel.query.filter_by(id=id).first()
    
    if form_model:
        try:
            db.session.delete(form_model)
        except:
            db.session.rollback()
        else:
            db.session.commit()
            flash(f"Дані успішно видалено (id: {id})", category='success')
    else:
        flash(f"Такого айді не існує! (id: {id})", category='error')
            
            
    return redirect(url_for('db_table'))
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
         
        user = User(username=form.username.data, email=form.email.data,
                    password=form.password.data)
        
        try:
            db.session.add(user)
        except:
            db.session.rollback()
        else:
            db.session.commit()
            flash("Registration successful", category = 'success')
            app.logger.info("Registration successful")
        
        return redirect(url_for('login'))
        
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    
    
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.emaii.data).first()
        
        if user and user.verify_password(form.password.data):
            
            login_user(user, remember=form.remember.data)
             
            flash('You have been logged in!', category='success')
            
            next = request.args.get('next')
            
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('account'))
            # return redirect(url_for('account'))
        else:
            flash('Login unsuccessful. Please check username and password.', category='warning')
    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have beed logged out', 'info')
    return redirect(url_for('index'))


@app.route('/db_user_table')
@login_required
def db_user_table():
    users = User.query.all()
    return  render_template('db_user_table.html', users=users)


@app.route('/account')
@login_required
def account():
    return render_template('account.html')
   