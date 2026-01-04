from flask import Blueprint, render_template , redirect , request , flash, session , url_for     #import the modules
from app import db
from app.models import Task
tasks_bp = Blueprint('tasks',__name__)

@tasks_bp.route('/', methods=['GET', 'POST'])
def view_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tasks = Task.query.filter_by(User_id=session['user_id']).all()
    return render_template('tasks.html',tasks = tasks)

@tasks_bp.route('/add',methods = ['GET' , 'POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    title = request.form.get('title')
    if title:
        new_task = Task(title=title , User_id = session['user_id'] , status="Pending")
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!' , 'success')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>' , methods = ['POST'])
def toggle_status(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    task = Task.query.get(task_id)
    if task:
        if task.status =="Pending" :
            task.status = "Working"
        elif task.status == "Working":
            task.status = "Completed"
        else:
            task.status = "Pending"
        db.session.commit()
        flash('Task status updated successfully!' , 'success')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/delete/<int:task_id>' , methods = ['POST'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    task = Task.query.get(task_id)
    if task and task.User_id == session['user_id']:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!' , 'success')
    else:
        flash('Unauthorized!', 'error')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear' , methods = ['POST'])
def clear_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    Task.query.filter_by(User_id=session['user_id']).delete()
    db.session.commit()
    flash('All tasks cleared!' , 'success')
    return redirect(url_for('tasks.view_tasks'))