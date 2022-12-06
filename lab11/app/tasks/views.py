from datetime import datetime, timezone, timedelta
import os
from flask import render_template, flash, current_app, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .. import db
from . import tasks_bp
from .forms import TaskForm, CategoryForm, CommentsForm
from .models import Task, Priority, Category, Progress, Comment
from ..account.models import User


@tasks_bp.route('/tasks', methods=['GET'])
@login_required
def tasks():
    # tasks_ = Task.query.all()
    tasks_ = Task.query.order_by(Task.priority.desc(),
                                 Task.deadline.asc()
                                 ).all()
    
    return render_template('tasks.html', tasks=tasks_)


@tasks_bp.route('/task/<int:id>', methods=['GET', 'POST'])
@login_required
def task(id):
    allow_to_comment = 0
    task_ = Task.query.get_or_404(id)
    
    form = CommentsForm()
    
    if current_user.id == task_.owner_id or any([current_user.id==user.id for user in task_.assigned_users]):
        allow_to_comment = 1
        
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(content=form.content.data,
                              commentator_id=current_user.get_id(),
                              task_id=id)
        
            try:
                db.session.add(comment)
            except:
                db.session.rollback()
            else:
                db.session.commit()

            return redirect(url_for('tasks.task', id=id)) 
        else:
            return redirect(url_for('account.login'))
        
    return render_template('task.html', task=task_, form=form, allow_to_comment=allow_to_comment)


@tasks_bp.route('/task/<int:id>/delete', methods=['GET'])
@login_required
def task_delete(id):
    task_ = Task.query.get_or_404(id)
    
    try:
        db.session.delete(task_)
    except:
        db.session.rollback()
    else:
        db.session.commit()
        flash("Task deleted", category='success')
        current_app.logger.info("Task deleted")
    
    return redirect(url_for('tasks.tasks'))



@tasks_bp.route('/task/<int:id>/update', methods=['GET', 'POST'])
@login_required
def task_update(id):
    task_ = Task.query.get_or_404(id)
    
    form = TaskForm(title=task_.title, description=task_.description,
                    deadline=task_.deadline, priority=task_.priority.value)
    
    if form.validate_on_submit():
        try:
            utc_deadline = form.deadline.data.astimezone(timezone.utc)
        except AttributeError:
            utc_deadline = form.deadline.data
            
        if current_user.is_authenticated:
            try:
                task_.title = form.title.data
                task_.description = form.description.data
                task_.deadline = utc_deadline
                task_.priority = Priority(int(form.priority.data))
                task_.category_id = form.category_id.data
                
                users = User.query.filter(User.id.in_([int(i) for i in form.assign_user_id.data])).all()
                task_.assigned_users = users
            except Exception as ex:
                db.session.rollback()
            else:
                db.session.commit()
                flash("Task updated", category='success')
                current_app.logger.info("Task updated")
                
                
            return redirect(url_for('tasks.task', id=task_.id)) 
                
        else:
            return redirect(url_for('account.login'))
  
    
    return render_template('task_form.html', form=form)
    


@tasks_bp.route('/task/create', methods=['GET', 'POST'])
@login_required
def task_add():
    form = TaskForm()
    
    if form.validate_on_submit():
        try:
            utc_deadline = form.deadline.data.astimezone(timezone.utc)
        except AttributeError:
            utc_deadline = form.deadline.data
            
        if current_user.is_authenticated:
            task_ = Task(title=form.title.data, description=form.description.data,
                        deadline=utc_deadline, priority=Priority(int(form.priority.data)),
                        category_id=form.category_id.data,
                        owner_id=current_user.get_id()) 

            # task.assigned_users = [User.query.get(int(i)) for i in form.assign_user_id.data]
            users = User.query.filter(User.id.in_([int(i) for i in form.assign_user_id.data])).all()
            task_.assigned_users = users
            
            try:
                db.session.add(task_)
            except:
                db.session.rollback()
            else:
                db.session.commit()
                flash("Task added", category='success')
                current_app.logger.info("Task added")

            return redirect(url_for('tasks.tasks')) 
        else:
            return redirect(url_for('account.login'))
        
    
    return render_template('task_form.html', form=form)



@tasks_bp.route('/categories', methods=['GET'])
@login_required
def categories():
    categories_ = Category.query.all()
    return render_template('categories.html', categories=categories_)


@tasks_bp.route('/category/create', methods=['GET', 'POST'])
@login_required
def category_add():
    form = CategoryForm()
    
    if form.validate_on_submit():
        if current_user.is_authenticated:
            category = Category(name=form.name.data) 

            try:
                db.session.add(category)
            except:
                db.session.rollback()
            else:
                db.session.commit()
                flash("Category added", category='success')
                current_app.logger.info("Category added")
        else:
            return redirect(url_for('account.login'))
  
    
    if request.method == 'POST':
        return redirect(url_for('tasks.categories')) 
    
    return render_template('category_form.html', form=form)



@tasks_bp.route('/categories/<int:id>/delete', methods=['GET'])
@login_required
def category_delete(id):
    category_ = Category.query.get_or_404(id)
    
    try:
        db.session.delete(category_)
    except:
        db.session.rollback()
    else:
        db.session.commit()
        flash("Category deleted", category='success')
        current_app.logger.info("Category deleted")
    
    return redirect(url_for('tasks.categories'))


@tasks_bp.route('/category/<int:id>/update', methods=['GET', 'POST'])
@login_required
def category_update(id):
    category_ = Category.query.get_or_404(id)
    
    form = CategoryForm(name=category_.name)
    
    if form.validate_on_submit():
        if current_user.is_authenticated:
            try:
                category_.name = form.name.data
            except:
                db.session.rollback()
            else:
                db.session.commit()
                flash("Category updated", category='success')
                current_app.logger.info("Category updated")
        else:
            return redirect(url_for('account.login'))
  
    if request.method == 'POST':
        return redirect(url_for('tasks.categories', id=category_.id)) 
    
    return render_template('category_form.html', form=form)
    

@tasks_bp.route('/task/<int:id>/up-progress', methods=['GET', ])
@login_required
def up_progress(id):
    
    task_ = Task.query.get_or_404(id)
    
    try:
        task_.progress = Progress(task_.progress.value + 1)
    except:
        db.session.rollback()
    else:
        db.session.commit()
        flash("Progress updated", category='success')
        current_app.logger.info("Progress updated")
        
    
    return redirect(url_for('tasks.task', id=id))

