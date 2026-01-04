from flask import Blueprint, render_template , redirect , request , flash, session , url_for    #import the modules
from app import db
from app.models import User

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('tasks.view_tasks'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in or use a different email.', 'error')
            return redirect(url_for('auth.register'))
        
        # Check if username already exists
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken. Please choose a different username.', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(username=username , email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()     #get the first user with that email

        if user and user.check_password(password):
            session['user_id'] = user.id    #storing user id in session
            flash('Login successful!', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)        
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))