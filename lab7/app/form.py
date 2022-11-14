from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from .models import User

SUBJECT_CHOICES = ['Math', 'English', 'History']

class Myform(FlaskForm):
    name = StringField("Candidate Name", 
                      [DataRequired("Please enter your name."), 
                       Length(min=4, max=10, message ='The length of this field must be 4-10 characters')
                       ]
                       )
    email = StringField('Email', validators=[DataRequired("Please enter your email."), Email("Please enter a valid email")])
    phone = StringField('Phone Number', validators=[DataRequired("Please enter your phone number."), Regexp(regex=r"^\+380\d{9}$", message='Please enter a valid number (+380xxxxxxxxx)')])
    subject = SelectField('Subject', validators=[DataRequired("Please choose subject.")], choices=SUBJECT_CHOICES)
    message = TextAreaField('Message', validators=[DataRequired("Please enter text."),
                                                   Length(max=500, message ='No more than 500 characters')])
    
    submit = SubmitField("Send")
    

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
    emaii =  StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),])
    remember = BooleanField('Remember me')
    
    submit = SubmitField('Login')

