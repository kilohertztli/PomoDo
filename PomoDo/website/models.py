from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    profile_img = db.Column(db.String(150))
    medals = db.Column(db.Integer, default=0)
    goals = db.Column(db.Integer, default=0)
    tasks = db.relationship('Task')
    sessions = db.relationship('Session')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cycles = db.relationship('Session', backref='task', lazy=True)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_type = db.Column(db.String(50), default='Pomodoro')  # 'pomodoro' or 'break'
    timestamp = db.Column(db.DateTime, default=datetime.now)
    duration_minutes = db.Column(db.Integer)
    skipped = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
