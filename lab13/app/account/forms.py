from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           [DataRequired(),
                            Length(min=4, max=14, message ='The length of this field must be 4-10 characters'),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'User must have only letters, numbers, dots or underscores')])
    email = StringField('Email', validators=[DataRequired("Please enter your email."), 
                                             Email("Please enter a valid email")])
    password = PasswordField('Password', [Length(min=6, message="The length of this field must be at least 6 characters"),
                                          EqualTo('confirm_password', message="Passwords must match")])
    confirm_password = PasswordField('Repeat Password')
    
    submit = SubmitField('Sign up')
    
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')
    
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),])
    remember = BooleanField('Remember me')
    
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           [DataRequired(),
                            Length(min=4, max=14, message ='The length of this field must be 4-10 characters'),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'User must have only letters, numbers, dots or underscores')])
    email = StringField('Email', validators=[DataRequired("Please enter your email."), 
                                             Email("Please enter a valid email")])
    about_me = CKEditorField('About Me', [Length(max=9999, message="The maximum length is 9999 characters")])
    image_file = FileField("Update Profile Picture",
                           validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')
    
    def validate_email(self, field):
        if field.data != current_user.email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already registered.')
    
    
    def validate_username(self, field):
        if field.data != current_user.username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already in use')
        


class UpdateAccountPasswordForm(FlaskForm):
    
    old_password = PasswordField('Old Password')
    
    password = PasswordField('Password', [Length(min=6, message="The length of this field must be at least 6 characters"),
                                          EqualTo('confirm_password', message="Passwords must match")])
    confirm_password = PasswordField('Repeat Password')
    
    submit = SubmitField('Update')
    

    