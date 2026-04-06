document.addEventListener("DOMContentLoaded", function() {
    // Lấy dữ liệu thật từ các thẻ input ẩn trong HTML
    const successCount = parseInt(document.getElementById("data-success")?.value) || 0;
    const failedCount = parseInt(document.getElementById("data-failed")?.value) || 0;

    // 1. Biểu đồ Doanh Thu (Line Chart)
    var ctxRevenue = document.getElementById("revenueChart");
    if (ctxRevenue) {
        new Chart(ctxRevenue, {
            type: 'line',
            data: {
                labels: ["T1", "T2", "T3", "T4", "T5", "T6"],
                datasets: [{
                    label: "Doanh thu",
                    lineTension: 0.3,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "rgba(78, 115, 223, 1)",
                    pointRadius: 3,
                    pointBackgroundColor: "rgba(78, 115, 223, 1)",
                    data: [0, 500, 1200, 800, 1600, 2450], 
                }],
            },
            options: { maintainAspectRatio: false, legend: { display: false } }
        });
    }

    // 2. Biểu đồ Security (Doughnut Chart - Dữ liệu thật)
    var ctxLogin = document.getElementById("loginChart");
    if (ctxLogin) {
        new Chart(ctxLogin, {
            type: 'doughnut',
            data: {
                labels: ["Hợp lệ", "Nghi ngờ"],
                datasets: [{
                    data: [successCount, failedCount], // DỮ LIỆU THẬT Ở ĐÂY
                    backgroundColor: ['#1cc88a', '#e74a3b'],
                    hoverBackgroundColor: ['#17a673', '#c0392b'],
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                }],
            },
            options: {
                maintainAspectRatio: false,
                cutoutPercentage: 70,
                legend: { display: false }
            },
        });
    }
});