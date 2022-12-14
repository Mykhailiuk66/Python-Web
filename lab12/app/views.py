from flask import render_template, request, redirect, flash, url_for, session, abort
from flask_login import login_user, current_user, logout_user, login_required

from app import app


@app.route('/delete_session')
def delete_session():
    session.pop('email', default=None)
    session.pop('username', default=None)
    return render_template('delete_page.html')
   

