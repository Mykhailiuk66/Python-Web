from flask import render_template, request, redirect, flash, url_for, session, abort, current_app
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlparse, urljoin

from .. import db
from .models import User
from .forms import RegistrationForm, LoginForm
from . import account_bp
from ..tasks.models import Progress

@account_bp.route('/test2')
def test2():
    return 'OK'


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


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
    user = User.query.get_or_404(id)
    
    tasks_info = {'TODO': 0, 'DOING': 0, 'DONE': 0}
    for task in user.assigned_tasks: tasks_info[task.progress.name] += 1
   
    return render_template('account.html', user=user, tasks_info=tasks_info)
