from flask import render_template, request, redirect, flash, url_for, session, abort, current_app
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlparse, urljoin
import os
import secrets
from PIL import Image
from pytz import UTC
from datetime import datetime 

from .. import db
from .models import User
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdateAccountPasswordForm
from . import account_bp
from ..tasks.models import Progress


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_nme, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static\profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn


@account_bp.before_request
def update_last_seen():
    if current_user.is_authenticated:
        datetime_ = datetime.now()
        utc_datetime_ = datetime_.astimezone(UTC)
            
        current_user.last_seen = utc_datetime_
        db.session.add(current_user) 
        db.session.commit()
        

@account_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

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
            flash("Registration successful", category='success')
            current_app.logger.info("Registration successful")

        return redirect(url_for('account.login'))

    return render_template('register.html', form=form)


@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account.account', id=current_user.id))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)

            flash('You have been logged in!', category='success')

            next = request.args.get('next')

            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('account.account', id=current_user.id))
        else:
            flash('Login unsuccessful. Please check username and password.', category='warning')

    return render_template('login.html', form=form)


@account_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home.index'))


@account_bp.route('/db_user_table')
@login_required
def db_user_table():
    users = User.query.all()
    return render_template('db_user_table.html', users=users)


@account_bp.route('/account/<int:id>')
@login_required
def account(id):
    if id == current_user.id:
        user = current_user
    else:
        user = User.query.get_or_404(id)
    
    tasks_info = {'TODO': 0, 'DOING': 0, 'DONE': 0}
    for task in user.assigned_tasks: tasks_info[task.progress.name] += 1
    
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    
    return render_template('account.html', user=user, tasks_info=tasks_info, 
                           image_file=image_file)



@account_bp.route('/account/<int:id>/update', methods=['GET', 'POST'])
@login_required
def account_update(id):
    if id != current_user.id:
        return redirect(url_for('account.account', id=id))
        
    form = UpdateAccountForm()
    if form.validate_on_submit():
        try:
            if form.image_file.data:
                image_file = save_picture(form.image_file.data)
                current_user.image_file = image_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.about_me = form.about_me.data
        except:
            db.session.rollback()
        else:
            db.session.commit()
            flash("Your account has been updated!", 'success')
            
        return redirect(url_for('account.account', id=id))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    
    
    return render_template('update_account.html', form=form, image_file=image_file)


@account_bp.route('/account/<int:id>/change-password', methods=['GET', 'POST'])
@login_required
def account_password_update(id):
    if id != current_user.id:
        return redirect(url_for('account.account', id=id))
        
    form = UpdateAccountPasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            try:
                current_user.password = form.password.data
            except:
                db.session.rollback()
            else:
                db.session.commit()
                flash("Your account password has been updated!", 'success')
        
            return redirect(url_for('account.account', id=id))
        else:
            flash("Wrong password!!!", 'warning')
    
    return render_template('update_account_password.html', form=form)


