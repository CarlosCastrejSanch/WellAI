from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Define the User Permission model
user_permissions = db.Table('user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email= db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    is_active = db.Column(db.Boolean, default=False)
    is_corp = db.Column(db.Boolean, default=False)
    is_doctor = db.Column(db.Boolean, default=False)
    is_employee =  db.Column(db.Boolean, default=False)
    role = db.Column(db.String(100), unique=False)
    gender = db.Column(db.String(100), unique=False)
    permissions = db.relationship('Permission', secondary=user_permissions, lazy='subquery',backref=db.backref('users', lazy=True))
    doctor_access = db.Column(db.Boolean, default=False)
    

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    
class EmployeeList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100), unique=False)
    role = db.Column(db.String(100), unique=False)
    gender = db.Column(db.String(100), unique=False)
    is_doctor = db.Column(db.Boolean, default=False)
    corp_id = db.Column(db.Integer, db.ForeignKey('user.id'))

