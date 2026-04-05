document.addEventListener("DOMContentLoaded", function() {
    
    // 1. CHỨC NĂNG ẨN/HIỆN MẬT KHẨU (Login / Register)
    const togglePassword = document.querySelector("#togglePassword");
    const password = document.querySelector("#password");
    const eyeIcon = document.querySelector("#eyeIcon");

    if (togglePassword && password && eyeIcon) {
        togglePassword.addEventListener("click", function () {
            const type = password.getAttribute("type") === "password" ? "text" : "password";
            password.setAttribute("type", type);
            
            if (type === "password") {
                eyeIcon.classList.remove("bi-eye-slash");
                eyeIcon.classList.add("bi-eye");
            } else {
                eyeIcon.classList.remove("bi-eye");
                eyeIcon.classList.add("bi-eye-slash");
            }
        });
    }

    // 2. CHỨC NĂNG THANH TRƯỢT SẢN PHẨM (Home Page)
    const track = document.getElementById("sliderTrack");
    const leftBtn = document.getElementById("slideLeft");
    const rightBtn = document.getElementById("slideRight");

    if(track && leftBtn && rightBtn) {
        leftBtn.addEventListener("click", () => {
            const scrollAmount = track.clientWidth / 2; 
            track.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
        });
        rightBtn.addEventListener("click", () => {
            const scrollAmount = track.clientWidth / 2; 
            track.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        });
    }
}); 
    // Nút Add to Cart
    const addToCartBtn = document.getElementById("addToCartBtn");
    if(addToCartBtn) {
        addToCartBtn.addEventListener("click", function() {
            // Hiện thông báo popup khi nhấn mua hàng
            alert("Successfully added to cart!");
        });
    }

    // Nút Tăng/Giảm số lượng
    const btnMinus = document.getElementById("btn-minus");
    const btnPlus = document.getElementById("btn-plus");
    const qtyInput = document.getElementById("qty-input");

    if(btnMinus && btnPlus && qtyInput) {
        btnMinus.addEventListener("click", () => {
            let val = parseInt(qtyInput.value);
            if(val > 1) { // Không cho giảm dưới 1
                qtyInput.value = val - 1;
            }
        });
        
        btnPlus.addEventListener("click", () => {
            let val = parseInt(qtyInput.value);
            let maxStock = 24; // Giả sử trong kho còn 24 cuốn
            if(val < maxStock) {
                qtyInput.value = val + 1;
            } else {
                alert("Maximum quantity reached!");
            }
        });
    }

document.addEventListener("DOMContentLoaded", function() {
    
    // ... (Các code cũ của bạn như Ẩn/Hiện mật khẩu, Slider, Thêm vào giỏ ở đây) ...

    // ========================================================
    // 4. CHỨC NĂNG TRANG GIỎ HÀNG (Cart Page)
    // ========================================================
    // Lấy tất cả các sản phẩm trong giỏ hàng
    const cartItems = document.querySelectorAll(".cart-item");
    
    cartItems.forEach(item => {
        // Tìm nút trừ, nút cộng và ô nhập số lượng của TỪNG sản phẩm
        const minusBtn = item.querySelector(".cart-minus");
        const plusBtn = item.querySelector(".cart-plus");
        const input = item.querySelector(".cart-qty");

        // Nếu tồn tại cả 3 thành phần này thì mới gắn sự kiện click
        if(minusBtn && plusBtn && input) {
            
            // Xử lý khi bấm nút Trừ (-)
            minusBtn.addEventListener("click", () => {
                let val = parseInt(input.value);
                if(val > 1) { // Số lượng không được nhỏ hơn 1
                    input.value = val - 1;
                }
            });
            
            // Xử lý khi bấm nút Cộng (+)
            plusBtn.addEventListener("click", () => {
                let val = parseInt(input.value);
                input.value = val + 1;
            });
            
        }
    });

    // Xử lý nút Update Quantity
    const updateCartBtn = document.getElementById("updateCartBtn");
    if(updateCartBtn) {
        updateCartBtn.addEventListener("click", function() {
            // Kiểm tra xem đã có thư viện toastr chưa để báo lỗi tránh sập JS
            if (typeof toastr !== 'undefined') {
                toastr.info("Updating quantity...", "Please wait");
                setTimeout(() => {
                    toastr.success("Update quantity successful!", "Success");
                }, 1000);
            } else {
                alert("Update quantity successful!");
            }
        });
    }

});