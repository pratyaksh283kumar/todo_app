#main database handling engine
from app import db  #importing the db object
#for password hashing
from werkzeug.security import generate_password_hash, check_password_hash


class Task(db.Model):   #creating the table "Task"
    id = db.Column(db.Integer , primary_key = True) #creating the main columns
    title = db.Column(db.String(100) , nullable = False)
    status = db.Column(db.String(20) ,default = "Pending")
    User_id = db.Column(db.Integer , db.ForeignKey('user.id'))  #foreign key relationship with User table

class User(db.Model):   #creating the table "User"
    id = db.Column(db.Integer , primary_key = True) #creating the main columns
    username = db.Column(db.String(50) , nullable = False , unique = True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128) , nullable = False)
    tasks = db.relationship('Task', backref='user', lazy=True)                  
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
