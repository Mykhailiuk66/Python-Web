from .. import db

class FormModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(100), nullable=False, unique=True)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(5000), nullable=False)
    
    def __repr__(self):
        return '%r' % self.name
    