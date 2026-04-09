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

# Số lượng lượt đăng nhập sai bạn muốn tạo ra (50 là con số đẹp để AI bắt được)
NUM_ATTEMPTS = 50 

def run_simulation():
    print(f"🚀  Attempting brute force attack on {TARGET_USERNAME}")
    print("-" * 60)
    
    for i in range(NUM_ATTEMPTS):
        # Lấy ngẫu nhiên một mật khẩu từ danh sách
        test_password = random.choice(DUMMY_PASSWORDS)
        
        # Dữ liệu gửi đi giống hệt như khi người dùng gõ vào form đăng nhập
        payload = {
            "username": TARGET_USERNAME,
            "password": test_password
        }
        
        try:
            # Gửi yêu cầu POST (giống hành động nhấn nút Login)
            response = requests.post(LOGIN_URL, data=payload)
            
            # In ra tiến trình để bạn theo dõi trong Terminal
            print(f"[{i+1}/{NUM_ATTEMPTS}] Thử: {TARGET_USERNAME} / {test_password:<10} | Status: {response.status_code}")
            
        except requests.exceptions.ConnectionError:
            print("\n❌ Error:  Server Flask!")
            print("👉 You need to run the app.py file before running this script.")
            break
            
        # Nghỉ một chút giữa các lần thử để giống người thật (hoặc tool xịn) hơn
        # Và tránh làm treo máy khi demo
        time.sleep(random.uniform(0.05, 0.2))

    print("-" * 60)
    print("✅ Simulation completed!")
    print("👉 Now, go to the Admin Panel (Logs) on the web to see the AI detect the brute force attack.")

if __name__ == "__main__":
    run_simulation()