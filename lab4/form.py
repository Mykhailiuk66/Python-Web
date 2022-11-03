from flask_wtf import FlaskForm  
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp


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