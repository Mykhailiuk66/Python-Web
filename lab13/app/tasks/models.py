from .. import db
from sqlalchemy.sql.functions import now
import enum

class Priority(enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Progress(enum.Enum):
    TODO = 1
    DOING = 2
    DONE = 3
 
    
assigned_task_user = db.Table('assigned_task_user',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
            )
    
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(2000), nullable=False)
    description = db.Column(db.String)
    created = db.Column(db.DateTime(timezone=True), server_default=now())
    modified = db.Column(db.DateTime(timezone=True), onupdate=now())
    deadline = db.Column(db.DateTime(timezone=True))
    priority = db.Column(db.Enum(Priority, values_callable=lambda x: [str(e.value) for e in Priority]), nullable=False, default=Priority(1))
    progress = db.Column(db.Enum(Progress, values_callable=lambda x: [str(e.value) for e in Progress]), nullable=False, default=Progress(1))

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
        
    owner = db.relationship('User', backref=db.backref('tasks'), foreign_keys=[owner_id])
    category = db.relationship('Category', backref=db.backref('tasks'), foreign_keys=[category_id])
    assigned_users = db.relationship('User', secondary=assigned_task_user, backref=db.backref('assigned_tasks'))


    def __repr__(self):
        return f"{self.title}"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)


    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)

    commentator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)    

    commentator = db.relationship('User', backref=db.backref('comments'), foreign_keys=[commentator_id])
    task = db.relationship('Task', backref=db.backref('comments'), foreign_keys=[task_id])

