document.addEventListener("DOMContentLoaded", function () {
    // Fetch Performance Overview
    fetch("http://localhost:5000/api/performance-overview")
        .then((response) => response.json())
        .then((data) => {
            document.getElementById(
                "flight-hours"
            ).textContent = `${data.flight_hours} hours`;
            document.getElementById(
                "total-flights"
            ).textContent = `${data.total_flights} flights`;
            document.getElementById(
                "completed-simulations"
            ).textContent = `${data.completed_simulations}`;
            document.getElementById(
                "unsuccessful-simulations"
            ).textContent = `${data.unsuccessful_simulations}`;
        });

    // Fetch Successful Flights Data
    function fetchSuccessfulFlights(timePeriod) {
        fetch(
            `http://localhost:5000/api/successful-flights?time_period=${timePeriod}`
        )
            .then((response) => response.json())
            .then((data) => {
                updateChart("score-chart", data);
            });
    }

    // Fetch Unsuccessful Flights Data
    function fetchUnsuccessfulFlights(timePeriod, airplaneModel) {
        fetch(
            `http://localhost:5000/api/unsuccessful-flights?time_period=${timePeriod}&airplane_model=${airplaneModel}`
        )
            .then((response) => response.json())
            .then((data) => {
                updateChart("time-chart", data);
            });
    }

    // Fetch Aircraft Damage Data
    function fetchAircraftDamage(timePeriod, airplaneModel) {
        fetch(
            `http://localhost:5000/api/aircraft-damage?time_period=${timePeriod}&airplane_model=${airplaneModel}`
        )
            .then((response) => response.json())
            .then((data) => {
                updateChart("damage-chart", data);
            });
    }

    // Update Chart Logic
    function updateChart(chartId, data) {
        const ctx = document.getElementById(chartId).getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: chartId,
                        data: data.success || data.failure || data.damage,
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                        borderColor: "rgba(75, 192, 192, 1)",
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        });
    }

    // Event listeners for selecting time period
    document
        .getElementById("time-period")
        .addEventListener("change", function () {
            const timePeriod = this.value;
            fetchSuccessfulFlights(timePeriod);
            fetchUnsuccessfulFlights(timePeriod, "all");
            fetchAircraftDamage(timePeriod, "Boeing 737");
        });

    document
        .getElementById("airplane-model")
        .addEventListener("change", function () {
            const airplaneModel = this.value;
            const timePeriod = document.getElementById("time-period").value;
            fetchUnsuccessfulFlights(timePeriod, airplaneModel);
        });

    document
        .getElementById("damage-time-period")
        .addEventListener("change", function () {
            const timePeriod = this.value;
            const airplaneModel = document.getElementById(
                "damage-airplane-model"
            ).value;
            fetchAircraftDamage(timePeriod, airplaneModel);
        });

    document
        .getElementById("damage-airplane-model")
        .addEventListener("change", function () {
            const airplaneModel = this.value;
            const timePeriod =
                document.getElementById("damage-time-period").value;
            fetchAircraftDamage(timePeriod, airplaneModel);
        });

    // Initial data load
    fetchSuccessfulFlights("monthly");
    fetchUnsuccessfulFlights("monthly", "all");
    fetchAircraftDamage("monthly", "Boeing 737");
});
