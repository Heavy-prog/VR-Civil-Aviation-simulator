document.addEventListener("DOMContentLoaded", function () {
    function toggleMenu() {
        const navMenu = document.querySelector("nav ul");
        navMenu.classList.toggle("active");
    }
    
    // Fetch and update Performance Overview
    function fetchPerformanceOverview() {
        document.getElementById("flight-hours").textContent = "50 ";
        document.getElementById("total-flights").textContent = "120 ";
        document.getElementById("completed-simulations").textContent =
            "100 ";
        document.getElementById("unsuccessful-simulations").textContent =
            "20 ";
    }

    // Successful Flights Chart
    const ctx1 = document.getElementById("score-chart").getContext("2d");
    const scoreChart = new Chart(ctx1, {
        type: "bar",
        data: {
            labels: ["Boeing 737", "Airbus A320", "Cessna 172", "Boing 777"],
            datasets: [
                {
                    label: "Successful Flights",
                    data: [12, 19, 3, 5],
                    backgroundColor: "#28a745",
                },
            ],
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });

    // Unsuccessful Flights Chart
    const ctx2 = document.getElementById("time-chart").getContext("2d");
    const timeChart = new Chart(ctx2, {
        type: "line",
        data: {
            labels: ["Flight 1", "Flight 2", "Flight 3", "Flight 4"],
            datasets: [
                {
                    label: "Unsuccessful Flights",
                    data: [1, 3, 0, 2],
                    borderColor: "#dc3545",
                    fill: false,
                },
            ],
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });

    // Aircraft Damage Analysis Chart
    const ctx3 = document.getElementById("damage-chart").getContext("2d");
    const damageChart = new Chart(ctx3, {
        type: "pie",
        data: {
            labels: ["Minor Damage", "Moderate Damage", "Severe Damage"],
            datasets: [
                {
                    label: "Damage Type",
                    data: [10, 5, 2],
                    backgroundColor: ["#ffc107", "#fd7e14", "#dc3545"],
                },
            ],
        },
        options: {
            responsive: true,
        },
    });

    // Update Chart Data Functions
    function updateSuccessfulFlights(timePeriod) {
        let data;
        if (timePeriod === "daily") {
            data = [5, 6, 7, 8];
        } else if (timePeriod === "weekly") {
            data = [15, 12, 10, 8];
        } else {
            data = [50, 45, 40, 35];
        }
        scoreChart.data.datasets[0].data = data;
        scoreChart.update();
    }

    function updateUnsuccessfulFlights(airplaneModel) {
        let data;
        if (airplaneModel === "Boeing 737") {
            data = [1, 4, 2, 0];
        } else if (airplaneModel === "Airbus A320") {
            data = [2, 3, 5, 1];
        } else if (airplaneModel === "Cessna 172") {
            data = [0, 1, 1, 0];
        } else {
            data = [1, 3, 0, 2];
        }
        timeChart.data.datasets[0].data = data;
        timeChart.update();
    }

    function updateAircraftDamage(timePeriod, airplaneModel) {
        let data;
        if (timePeriod === "daily") {
            if (airplaneModel === "Boeing 737") {
                data = [3, 2, 1];
            } else if (airplaneModel === "Airbus A320") {
                data = [4, 1, 2];
            } else {
                data = [2, 3, 1];
            }
        } else if (timePeriod === "weekly") {
            data = [7, 5, 3];
        } else {
            data = [20, 10, 5];
        }
        damageChart.data.datasets[0].data = data;
        damageChart.update();
    }

    // Event Listeners
    document
        .getElementById("time-period")
        .addEventListener("change", function () {
            const timePeriod = this.value;
            updateSuccessfulFlights(timePeriod);
        });

    document
        .getElementById("airplane-model")
        .addEventListener("change", function () {
            const airplaneModel = this.value;
            updateUnsuccessfulFlights(airplaneModel);
        });

    document
        .getElementById("damage-time-period")
        .addEventListener("change", function () {
            const timePeriod = this.value;
            const airplaneModel =
                document.getElementById("damage-airplane-model").value;
            updateAircraftDamage(timePeriod, airplaneModel);
        });

    document
        .getElementById("damage-airplane-model")
        .addEventListener("change", function () {
            const airplaneModel = this.value;
            const timePeriod =
                document.getElementById("damage-time-period").value;
            updateAircraftDamage(timePeriod, airplaneModel);
        });

    // Initialize
    fetchPerformanceOverview();
});
