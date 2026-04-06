# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, LoginAttempt
import os

app = Flask(__name__)

# --- CẤU HÌNH HỆ THỐNG ---
# Secret key để bảo mật Session và Flash messages
app.secret_key = 'mot_chuoi_bi_mat_bat_ky_an_toan' 
# Đường dẫn tới file cơ sở dữ liệu SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo Database với App
db.init_app(app)

# Tự động tạo các bảng nếu chưa tồn tại
with app.app_context():
    db.create_all()

# --- CÁC ROUTE GIAO DIỆN ---

@app.route('/')
def home():
    """Trang chủ hiển thị sản phẩm"""
    return render_template('home.html')

@app.route('/product')
def product_detail():
    """Trang chi tiết của một cuốn sách cụ thể"""
    return render_template('product-detail.html')

@app.route('/cart')
def cart():
    """Trang giỏ hàng của người dùng"""
    return render_template('cart.html')

# --- HỆ THỐNG ĐĂNG KÝ / ĐĂNG NHẬP ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # 1. Kiểm tra xem người dùng đã tồn tại chưa
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one!', 'danger')
            return redirect(url_for('register'))

        # 2. Mã hóa mật khẩu bảo mật
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            # Thông báo thành công sẽ hiển thị dạng Toastr ở trang Login
            flash('Account registered successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while saving data.', 'danger')
            return redirect(url_for('register'))
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        client_ip = request.remote_addr # Lấy IP để phục vụ nghiên cứu Brute Force
        
        user = User.query.filter_by(username=username).first()
        
        # Kiểm tra sự tồn tại của user và khớp mật khẩu
        if user and check_password_hash(user.password, password):
            # LƯU VÀO SESSION (Dùng key 'username' để base.html nhận diện hiện icon người)
            session['username'] = user.username
            session['role'] = user.role
            
            # Ghi log: Đăng nhập THÀNH CÔNG (Dữ liệu cho mô hình AI SVM/Random Forest)
            attempt = LoginAttempt(username_tried=username, ip_address=client_ip, status='success')
            db.session.add(attempt)
            db.session.commit()
            
            flash(f'Login successful. Welcome back, {username}!', 'success')
            return redirect(url_for('home'))
        else:
            # Ghi log: Đăng nhập THẤT BẠI
            attempt = LoginAttempt(username_tried=username, ip_address=client_ip, status='failed')
            db.session.add(attempt)
            db.session.commit()
            
            flash('Invalid username or password!', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Đăng xuất và xóa session"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if 'username' not in session:
        flash('Please log in to view your profile!', 'danger')
        return redirect(url_for('login'))
    
    # Lấy thông tin user từ Database
    user = User.query.filter_by(username=session['username']).first()
    
    return render_template('profile.html', user=user)

# --- KHỞI CHẠY SERVER ---
if __name__ == '__main__':
    # debug=True giúp server tự động load lại mỗi khi bạn sửa code
    app.run(debug=True)