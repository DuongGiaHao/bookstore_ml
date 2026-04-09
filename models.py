from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')

class LoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username_tried = db.Column(db.String(100))
    ip_address = db.Column(db.String(50))
    # Đã cập nhật default=datetime.now để lấy giờ Việt Nam chuẩn
    timestamp = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20)) # 'success', 'failed', 'brute_force'