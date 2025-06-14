from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from .models import Task, Session
from . import db

timer = Blueprint('timer', __name__)

@timer.route('/timer', methods=['GET', 'POST'])
@login_required
def pomodoro_timer():
    if request.method == 'POST':
        task = request.form.get('task')

        if len(task) < 1:
            flash('Enter a task!', category='error')
        else:
            new_task = Task(name=task, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added!', category='success')

    return render_template("timer.html", user=current_user)

@timer.route('/log-session', methods=['POST'])
@login_required
def log_session():
    data = request.get_json()

    task_id = data.get('task_id')
    session_type = data.get('session_type')
    duration = data.get('duration')
    skipped = data.get('skipped', False)

    if not task_id or not session_type or not duration:
        return jsonify({'status': 'error', 'message': 'Missing data!'}), 400

    new_session = Session(
        user_id=current_user.id,
        task_id=task_id,
        session_type=session_type,
        duration_minutes=duration,
        skipped=skipped
    )
    db.session.add(new_session)
    db.session.commit()

    update_goals(current_user)
    return jsonify({'status': 'success', 'message': 'Session added!'})

@timer.route('/delete-task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
   task = Task.query.get_or_404(task_id)

   if task.user_id != current_user.id:
       flash('You can\'t delete this task!', category='error')
       return redirect(url_for('timer.pomodoro_timer'))

   db.session.delete(task)
   db.session.commit()
   return redirect(url_for('timer.pomodoro_timer'))


def update_goals(user):
    today = date.today()
    start_of_day = datetime(today.year, today.month, today.day)
    end_of_day = start_of_day + timedelta(days=1)

    sessions_today = Session.query.filter(
        Session.user_id == user.id,
        Session.session_type == 'Pomodoro',
        # Session.skipped == False,
        Session.timestamp >= start_of_day,
        Session.timestamp < end_of_day
    ).count()

    user.goals = sessions_today
    goal_reached = False

    if sessions_today == 4:
        goal_reached = True

    if goal_reached:
        user.medals += 1

    db.session.commit()
