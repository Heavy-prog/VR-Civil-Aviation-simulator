document.addEventListener("DOMContentLoaded", function () {
    // Fetch Performance Overview
    fetch('/api/performance-overview')
        .then(response => response.json())
        .then(data => {
            document.getElementById('flight_hours').textContent = `${data.total_score}%`;
            document.getElementById('total_flights').textContent = `${data.time_spent} minutes`;
            document.getElementById('completed_simulations').textContent = `${data.completion}%`;
            document.getElementById('unsuccessful_simulations').textContent = `${data.total_score}%`;
        });

    // Fetch Successful Flights Data
    function fetchSuccessfulFlights(timePeriod) {
        fetch(`/api/successful-flights?time_period=${timePeriod}`)
            .then(response => response.json())
            .then(data => {
                updateChart('score-chart', data);
            });
    }

    // Fetch Unsuccessful Flights Data
    function fetchUnsuccessfulFlights(timePeriod, airplaneModel) {
        fetch(`/api/unsuccessful-flights?time_period=${timePeriod}&airplane_model=${airplaneModel}`)
            .then(response => response.json())
            .then(data => {
                updateChart('time-chart', data);
            });
    }

    // Fetch Aircraft Damage Data
    function fetchAircraftDamage(timePeriod, airplaneModel) {
        fetch(`/api/aircraft-damage?time_period=${timePeriod}&airplane_model=${airplaneModel}`)
            .then(response => response.json())
            .then(data => {
                updateChart('damage-chart', data);
            });
    }

    // Update Chart Logic
    function updateChart(chartId, data) {
        const ctx = document.getElementById(chartId).getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: chartId,
                    data: data.success || data.failure || data.damage,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Event listeners for selecting time period
    document.getElementById('time-period').addEventListener('change', function () {
        const timePeriod = this.value;
        fetchSuccessfulFlights(timePeriod);
        fetchUnsuccessfulFlights(timePeriod, 'all');
        fetchAircraftDamage(timePeriod, 'Boeing 737');
    });

    document.getElementById('airplane-model').addEventListener('change', function () {
        const airplaneModel = this.value;
        const timePeriod = document.getElementById('time-period').value;
        fetchUnsuccessfulFlights(timePeriod, airplaneModel);
    });

    document.getElementById('damage-time-period').addEventListener('change', function () {
        const timePeriod = this.value;
        const airplaneModel = document.getElementById('damage-airplane-model').value;
        fetchAircraftDamage(timePeriod, airplaneModel);
    });

    document.getElementById('damage-airplane-model').addEventListener('change', function () {
        const airplaneModel = this.value;
        const timePeriod = document.getElementById('damage-time-period').value;
        fetchAircraftDamage(timePeriod, airplaneModel);
    });

    // Initial data load
    fetchSuccessfulFlights('monthly');
    fetchUnsuccessfulFlights('monthly', 'all');
    fetchAircraftDamage('monthly', 'Boeing 737');
});
