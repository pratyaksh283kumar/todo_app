# Flask application initialization
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#create database object globally
db = SQLAlchemy()

#main app function
def create_app():
    app = Flask(__name__)   #main app (an object made using the Flask class in flask module)
    app.config['SECRET_KEY'] = 'pratyaksh_secret_key_7280'  #setting seret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'    #location of our database 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    #..??

    db.__init__(app) # connecting the db object to app

    #importing the custom modules , funcx made in the ./app/routes/auth in lines (18,19)
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    
    #registering blueprints(or mini apps to the Flask engine)
    app.register_blueprint(auth_bp)     
    app.register_blueprint(tasks_bp, url_prefix='/tasks')    

    return app  #returning the app