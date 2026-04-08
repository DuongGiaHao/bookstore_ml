import requests
import time
import random

# --- CẤU HÌNH ---
# Đường dẫn đến trang đăng nhập local của bạn
LOGIN_URL = "http://127.0.0.1:5000/login"

# Tài khoản mục tiêu bạn muốn giả vờ tấn công
TARGET_USERNAME = "admin"

# Danh sách các mật khẩu phổ biến thường bị hacker dùng để dò rỉ
DUMMY_PASSWORDS = [
    "123456", "password", "123456789", "12345", "12345678", 
    "admin", "admin123", "qwerty", "111111", "iloveyou"
]

# Số lượng lượt đăng nhập sai bạn muốn tạo ra
NUM_ATTEMPTS = 50 

def run_simulation():
    print(f"🚀 Brute Force Simulation: {TARGET_USERNAME}")
    print("-" * 50)
    
    for i in range(NUM_ATTEMPTS):
        # Lấy ngẫu nhiên một mật khẩu từ danh sách
        test_password = random.choice(DUMMY_PASSWORDS)
        
        # Dữ liệu gửi đi giống hệt như khi người dùng gõ vào form HTML
        payload = {
            "username": TARGET_USERNAME,
            "password": test_password
        }
        
        try:
            # Gửi yêu cầu POST (submit form)
            response = requests.post(LOGIN_URL, data=payload)
            
            print(f"[{i+1}/{NUM_ATTEMPTS}] Thử: {TARGET_USERNAME} / {test_password:<10} | Mã phản hồi: {response.status_code}")
            
        except requests.exceptions.ConnectionError:
            print("❌ Error: Server Flask not running! Please run app.py first.")
            break
            
        # Dừng một chút (từ 0.1 đến 0.5 giây) giữa các lần thử
        # Việc này giúp mô phỏng giống với các tool tấn công thực tế và không làm sập server local
        time.sleep(random.uniform(0.1, 0.5))

    print("-" * 50)
    print("✅ Simulation completed!")
    print("Now check the Admin Panel's Logs page to see the recorded login attempts and AI predictions.")

if __name__ == "__main__":
    run_simulation()