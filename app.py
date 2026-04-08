# app.py
import warnings
# Ẩn các cảnh báo về phiên bản thư viện để Terminal sạch sẽ khi demo
warnings.filterwarnings("ignore", category=UserWarning)

print("--- SERVER IS STARTING ---")

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, LoginAttempt
from datetime import datetime, timedelta
import os
import joblib
import numpy as np
import time 

app = Flask(__name__)

# --- CẤU HÌNH HỆ THỐNG ---
app.secret_key = 'mot_chuoi_bi_mat_bat_ky_an_toan' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo Database với App
db.init_app(app)

# --- XỬ LÝ ĐƯỜNG DẪN MÔ HÌNH THÔNG MINH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Đường dẫn chính xác tới thư mục model_ml của bạn
SVM_PATH = os.path.join(BASE_DIR, 'model_ml', 'model_svm.pkl')
RF_PATH = os.path.join(BASE_DIR, 'model_ml', 'model_rf.pkl')

# --- NẠP MÔ HÌNH MACHINE LEARNING ---
try:
    svm_model = joblib.load(SVM_PATH)
    rf_model = joblib.load(RF_PATH)
    print(f"✅ Models loaded successfully from: model_ml")
except Exception as e:
    print(f"⚠️ Failed to load AI models. Error details: {e}")
    svm_model = None
    rf_model = None

# Tự động tạo các bảng và tài khoản Admin
with app.app_context():
    db.create_all()
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        hashed_pw = generate_password_hash('admin123')
        try:
            new_admin = User(username='admin', email='admin@bookstore.com', password=hashed_pw, role='admin')
            db.session.add(new_admin)
        except TypeError:
            new_admin = User(username='admin', email='admin@bookstore.com', password=hashed_pw)
            db.session.add(new_admin)
        db.session.commit()
        print("✅ Created Admin: admin / admin123")

# --- HÀM AI DỰ ĐOÁN TẤN CÔNG BRUTE FORCE ---
def is_brute_force_attack(ip_address, username):
    if not svm_model: 
        return False
        
    # SỬA TẠI ĐÂY: Sử dụng datetime.now() để khớp với giờ Việt Nam trong Database
    time_threshold = datetime.now() - timedelta(minutes=5)
    
    failed_ip_count = LoginAttempt.query.filter(
        LoginAttempt.ip_address == ip_address,
        LoginAttempt.status == 'failed',
        LoginAttempt.timestamp >= time_threshold
    ).count()
    
    failed_user_count = LoginAttempt.query.filter(
        LoginAttempt.username_tried == username,
        LoginAttempt.status == 'failed',
        LoginAttempt.timestamp >= time_threshold
    ).count()
    
    features = np.array([[failed_ip_count, failed_user_count]])
    
    try:
        prediction = svm_model.predict(features)
        # Trả về True nếu AI dự đoán là 1 (Tấn công)
        return prediction[0] == 1
    except Exception as e:
        print(f"Error occurred while AI predicting: {e}")
        return False

# --- CÁC ROUTE GIAO DIỆN KHÁCH HÀNG ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/product')
def product_detail():
    return render_template('product-detail.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

# --- HỆ THỐNG ĐĂNG KÝ / ĐĂNG NHẬP ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account registered successfully!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            return redirect(url_for('register'))
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        client_ip = request.remote_addr 
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            if hasattr(user, 'role'):
                session['role'] = user.role
            
            attempt = LoginAttempt(username_tried=username, ip_address=client_ip, status='success')
            db.session.add(attempt)
            db.session.commit()
            
            if user.username == 'admin' or session.get('role') == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('home'))
        else:
            attempt = LoginAttempt(username_tried=username, ip_address=client_ip, status='failed')
            db.session.add(attempt)
            db.session.commit() 
            
            # Kiểm tra tấn công bằng AI
            is_attack = is_brute_force_attack(client_ip, username)
            
            if is_attack:
                attempt.status = 'brute_force'
                db.session.commit()
                flash('🚨 Warning: Systems AI detected a Brute Force attack!', 'danger')
            else:
                flash('Invalid username or password!', 'warning')
            
    return render_template('login.html')

# --- KHU VỰC ADMIN ---

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'username' not in session or (session.get('username') != 'admin' and session.get('role') != 'admin'):
        flash('You do not have permission to access this page!', 'danger')
        return redirect(url_for('home'))
        
    try:
        total_users = User.query.filter(User.role != 'admin').count()
    except AttributeError:
        total_users = User.query.filter(User.username != 'admin').count()
        
    success_logins = LoginAttempt.query.filter_by(status='success').count()
    failed_logins = LoginAttempt.query.filter_by(status='failed').count()
    brute_force_attacks = LoginAttempt.query.filter_by(status='brute_force').count()
    
    return render_template('admin/index.html', 
                           total_users=total_users,
                           failed_logins=failed_logins + brute_force_attacks,
                           success_logins=success_logins,
                           total_revenue=0,
                           total_orders=0)

@app.route('/admin/logs')
def admin_logs():
    if 'username' not in session or (session.get('username') != 'admin' and session.get('role') != 'admin'):
        return redirect(url_for('home'))
    # Sắp xếp Log mới nhất lên đầu
    all_logs = LoginAttempt.query.order_by(LoginAttempt.timestamp.desc()).all()
    return render_template('admin/logs.html', logs=all_logs)

@app.route('/admin/speed-test')
def admin_speed_test():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('home'))
        
    if not svm_model or not rf_model:
        flash('Models not loaded!', 'danger')
        return redirect(url_for('admin_dashboard'))

    num_samples = 10000
    test_features = np.random.randint(0, 20, size=(num_samples, 2))

    # Test SVM
    start_time_svm = time.time()
    svm_model.predict(test_features)
    svm_total_time = time.time() - start_time_svm

    # Test RF
    start_time_rf = time.time()
    rf_model.predict(test_features)
    rf_total_time = time.time() - start_time_rf

    return render_template('admin/speed_test.html', 
                           num_samples=num_samples,
                           svm_total_time=round(svm_total_time, 4),
                           rf_total_time=round(rf_total_time, 4),
                           svm_time_per_sample=round((svm_total_time / num_samples) * 1000, 5),
                           rf_time_per_sample=round((rf_total_time / num_samples) * 1000, 5))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout successful.', 'info')
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'username' not in session: return redirect(url_for('login'))
    user = User.query.filter_by(username=session['username']).first()
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)