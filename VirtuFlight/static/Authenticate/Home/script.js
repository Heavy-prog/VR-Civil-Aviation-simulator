// Toggle mobile navigation
function toggleMenu() {
    const nav = document.querySelector('nav');
    nav.classList.toggle('active');
}

// Smooth scrolling
function smoothScroll(target) {
    const element = document.querySelector(target);
    window.scrollTo({
        top: element.offsetTop - 60,
        behavior: 'smooth'
    });
}

// Start Simulator Button
document.getElementById('start-button').addEventListener('click', function() {
    alert("Starting VirtuFlight Simulator...");
    // Here you can link to the VR experience or another page
});
