from flask_login import UserMixin
from .. import db, bcrypt, login_manager
from flask import current_app as app
    
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    # password = db.Column(db.String(60), nullable=False)
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')
    
    
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)
    
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"