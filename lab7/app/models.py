from . import db, bcrypt

class FormModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(100), nullable=False, unique=True)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(5000), nullable=False)
    
    
        
    def __repr__(self):
        return '%r' % self.name
    

class User(db.Model):
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