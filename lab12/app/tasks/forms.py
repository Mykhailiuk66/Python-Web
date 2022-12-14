from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Optional
from flask_ckeditor import CKEditorField
from .models import Priority, Progress, Category
from ..account.models import User
from .. import db

class TaskForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_id.choices = [(category.id, category.name) for category in db.session.query(Category).all()]
        self.assign_user_id.choices = [(user.id, user.username) for user in db.session.query(User).all()]

    
    title = StringField('Title', [DataRequired()])
    description = CKEditorField('Description', [Length(max=2000, message="The maximum length is 2000 characters")])
    category_id = SelectField('Category') 
    assign_user_id = SelectMultipleField('Assign User (hold "Ctrl" to select multiple)', validate_choice=False) 
    deadline = DateTimeField('Deadline', format="%Y-%m-%dT%H:%M", validators=(Optional(),))
    priority = SelectField('Priority', choices=[(member.value, name.capitalize()) for name, member in Priority.__members__.items()])

    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    
    submit = SubmitField('Submit')


class CommentsForm(FlaskForm):
    content = CKEditorField('Description', [Length(max=2000, message="The maximum length is 2000 characters")])
    
    submit = SubmitField('Send')