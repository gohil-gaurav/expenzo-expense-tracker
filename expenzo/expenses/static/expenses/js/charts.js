document.addEventListener("DOMContentLoaded", function () {

    /* ================= CATEGORY DOUGHNUT CHART ================= */
    const categoryCtx = document.getElementById("categoryChart");

    if (categoryCtx && typeof Chart !== "undefined") {
        new Chart(categoryCtx, {
            type: "doughnut",
            data: {
                labels: categoryLabels,
                datasets: [{
                    data: categoryTotals,
                    backgroundColor: [
                        "#3b82f6", // blue
                        "#22c55e", // green
                        "#ef4444", // red
                        "#f59e0b", // amber
                        "#a855f7", // purple
                        "#14b8a6"  // teal
                    ],
                    borderWidth: 2,
                    borderColor: "#020617"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "65%",
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            color: "#e5e7eb",
                            padding: 15
                        }
                    },
                    tooltip: {
                        backgroundColor: "#020617",
                        titleColor: "#e5e7eb",
                        bodyColor: "#e5e7eb"
                    }
                }
            }
        });
    }

    /* ================= MONTHLY BAR CHART ================= */
const monthlyCtx = document.getElementById("monthlyChart");

if (monthlyCtx && typeof Chart !== "undefined") {
    new Chart(monthlyCtx, {
        type: "bar",
        data: {
            labels: monthLabels,
            datasets: [{
                label: "Monthly Expense",
                data: monthTotals,
                backgroundColor: "#ef4444",
                borderRadius: 10,
                maxBarThickness: 45
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: "#e5e7eb"
                    }
                },
                tooltip: {
                    backgroundColor: "#020617",
                    titleColor: "#e5e7eb",
                    bodyColor: "#e5e7eb",
                    callbacks: {
                        title: function (tooltipItems) {
                            // Shows month & year
                            return "Month: " + tooltipItems[0].label;
                        },
                        label: function (tooltipItem) {
                            return "Total Expense: ₹ " + tooltipItem.formattedValue;
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: { color: "#cbd5f5" },
                    grid: { display: false }
                },
                y: {
                    ticks: { color: "#cbd5f5" },
                    grid: { color: "rgba(255,255,255,0.05)" }
                }
            }
        }
    });
}


});
