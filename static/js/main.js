document.addEventListener("DOMContentLoaded", function () {

    // ========================================================
    // 1. CHỨC NĂNG ẨN/HIỆN MẬT KHẨU (Login / Register)
    // ========================================================
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

    // ========================================================
    // 2. CHỨC NĂNG THANH TRƯỢT SẢN PHẨM (Home Page)
    // ========================================================
    const track = document.getElementById("sliderTrack");
    const leftBtn = document.getElementById("slideLeft");
    const rightBtn = document.getElementById("slideRight");

    if (track && leftBtn && rightBtn) {
        leftBtn.addEventListener("click", () => {
            const scrollAmount = track.clientWidth / 2;
            track.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
        });
        rightBtn.addEventListener("click", () => {
            const scrollAmount = track.clientWidth / 2;
            track.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        });
    }

    // ========================================================
    // 3. CHỨC NĂNG TRANG CHI TIẾT SẢN PHẨM (Product Detail)
    // ========================================================
    const addToCartBtn = document.getElementById("addToCartBtn");
    const cartBadge = document.querySelector(".bi-cart3")?.parentElement.querySelector(".badge");
    const qtyInputDetail = document.getElementById("qty-input");
    const btnMinusDetail = document.getElementById("btn-minus");
    const btnPlusDetail = document.getElementById("btn-plus");

    // Nút Add to Cart & Cập nhật badge Navbar
    if (addToCartBtn) {
        addToCartBtn.addEventListener("click", function () {
            let qtyToAdd = qtyInputDetail ? parseInt(qtyInputDetail.value) : 1;

            if (cartBadge) {
                let currentQty = parseInt(cartBadge.innerText) || 0;
                cartBadge.innerText = currentQty + qtyToAdd;
            }

            if (typeof toastr !== 'undefined') {
                toastr.success(`Successfully added ${qtyToAdd} items to cart!`, "Success");
            } else {
                alert("Successfully added to cart!");
            }
        });
    }

    // Bộ tăng giảm số lượng trang chi tiết
    if (btnMinusDetail && btnPlusDetail && qtyInputDetail) {
        btnMinusDetail.addEventListener("click", () => {
            let val = parseInt(qtyInputDetail.value);
            if (val > 1) qtyInputDetail.value = val - 1;
        });
        btnPlusDetail.addEventListener("click", () => {
            let val = parseInt(qtyInputDetail.value);
            if (val < 24) { // Giả sử kho còn 24
                qtyInputDetail.value = val + 1;
            } else {
                toastr.warning("Maximum quantity reached!");
            }
        });
    }

    // ========================================================
    // 4. CHỨC NĂNG TRANG GIỎ HÀNG (Cart Calculation)
    // ========================================================
    const cartItems = document.querySelectorAll(".cart-item");
    if (cartItems.length > 0) {
        cartItems.forEach(item => {
            const minusBtn = item.querySelector(".cart-minus");
            const plusBtn = item.querySelector(".cart-plus");
            const input = item.querySelector(".cart-qty");

            if (minusBtn && plusBtn && input) {
                minusBtn.addEventListener("click", () => {
                    let val = parseInt(input.value);
                    if (val > 1) input.value = val - 1;
                });
                plusBtn.addEventListener("click", () => {
                    let val = parseInt(input.value);
                    input.value = val + 1;
                });
            }
        });
    }

    const updateCartBtn = document.getElementById("updateCartBtn");
    if (updateCartBtn) {
        updateCartBtn.addEventListener("click", function () {
            let bagTotal = 0;
            const allItems = document.querySelectorAll(".cart-item");

            allItems.forEach(item => {
                const priceElement = item.querySelector(".item-price");
                const qtyInput = item.querySelector(".cart-qty");
                
                if (priceElement && qtyInput) {
                    const price = parseFloat(priceElement.getAttribute("data-price"));
                    const qty = parseInt(qtyInput.value);
                    bagTotal += price * qty;
                }
            });

            const tax = bagTotal * 0.1;
            const totalAmount = bagTotal + tax;

            // Cập nhật giao diện Order Summary
            if (document.getElementById("summary-bag-total")) {
                document.getElementById("summary-bag-total").innerText = `$${bagTotal.toFixed(2)}`;
                document.getElementById("summary-tax").innerText = `$${tax.toFixed(2)}`;
                document.getElementById("summary-total-amount").innerText = `$${totalAmount.toFixed(2)}`;
            }

            if (typeof toastr !== 'undefined') {
                toastr.success("Cart updated successfully!");
            }
        });
    }

    // ========================================================
    // 5. HIỂN THỊ FLASH MESSAGES TỪ FLASK (Toastr)
    // ========================================================
    const flashData = document.getElementById('flash-data');
    if (flashData) {
        const messages = flashData.querySelectorAll('.msg');
        messages.forEach(m => {
            const text = m.innerText;
            const category = m.getAttribute('data-category'); // success, danger, info...

            toastr.options = {
                "closeButton": true,
                "progressBar": true,
                "positionClass": "toast-top-right",
                "timeOut": "4000"
            };

            if (category === 'success') {
                toastr.success(text);
            } else if (category === 'danger' || category === 'error') {
                toastr.error(text);
            } else {
                toastr.info(text);
            }
        });
    }
});