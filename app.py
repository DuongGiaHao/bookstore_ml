# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, LoginAttempt
import os

app = Flask(__name__)
# Thiết lập bảo mật cho Session và Flash messages
app.secret_key = 'mot_chuoi_bi_mat_bat_ky_an_toan' 
# Đường dẫn tới file SQLite (sẽ tự tạo trong cùng thư mục)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo DB với app
db.init_app(app)

# Tạo các bảng trong database trước khi request đầu tiên chạy
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Kiểm tra user tồn tại chưa
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        # Mã hóa mật khẩu trước khi lưu
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Register successful. Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        client_ip = request.remote_addr # Lấy IP của người dùng
        
        user = User.query.filter_by(username=username).first()
        
        # Kiểm tra mật khẩu
        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            session['role'] = user.role
            
            # Ghi log: Đăng nhập thành công
            attempt = LoginAttempt(username_tried=username, ip_address=client_ip, status='success')
            db.session.add(attempt)
            db.session.commit()
            
            flash(f'Chào mừng {username}!', 'success')
            return redirect(url_for('home'))
        else:
            # Ghi log: Đăng nhập thất bại (Dữ liệu quan trọng cho mô hình phân loại sau này)
            attempt = LoginAttempt(username_tried=username, ip_address=client_ip, status='failed')
            db.session.add(attempt)
            db.session.commit()
            
            flash('Sai tên đăng nhập hoặc mật khẩu!', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)