// Update slider values dynamically
document.querySelectorAll('input[type="range"]').forEach(slider => {
    const valueDisplay = slider.previousElementSibling.querySelector('.value');
    slider.addEventListener('input', event => {
        const value = event.target.value;
        valueDisplay.textContent = value; // Update the value display
    });
});

// Start Simulation Button Functionality
document.getElementById('start-btn').addEventListener('click', () => {
    alert('Simulation Started! Adjust the parameters as required.');
});

// Terrain Selection Functionality
document.querySelectorAll('.terrain').forEach(terrain => {
    terrain.addEventListener('click', () => {
        // Remove selected class from all terrains
        document.querySelectorAll('.terrain').forEach(item => {
            item.classList.remove('selected');
        });
        // Add selected class to the clicked terrain
        terrain.classList.add('selected');
        // Update terrain name in the console (for reference)
        console.log('Selected Terrain:', terrain.getAttribute('data-terrain'));
    });
});
document.querySelector('#add-condition-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch('/flight_conditions', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Flight condition added successfully!');
                location.reload();
            }
        });
});

