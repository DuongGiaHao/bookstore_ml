# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Lưu mật khẩu đã mã hóa (hash)
    role = db.Column(db.String(10), default='user')

 # Bảng thu thập dữ liệu để sau này tích hợp mô hình học máy chống Brute Force
class LoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username_tried = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False) # 'success' hoặc 'failed'