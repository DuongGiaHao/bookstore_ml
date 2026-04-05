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