document.getElementById('auth-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.redirect) {
                window.location.href = data.redirect;
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

// Admin sign-in button click event
document.getElementById('admin-btn').addEventListener('click', function() {
    document.getElementById('form-title').textContent = "Admin Sign In";
    document.getElementById('auth-form').style.display = 'block';
    document.getElementById('username').value = "admin";
    document.getElementById('password').value = "admin";
});

// Pilot sign-in button click event
document.getElementById('pilot-btn').addEventListener('click', function() {
    document.getElementById('form-title').textContent = "Pilot Sign In";
    document.getElementById('auth-form').style.display = 'block';
    document.getElementById('username').value = "PK-01";
    document.getElementById('password').value = "pilot";
});

// Validate sign-in credentials and handle the admin redirection
document.getElementById('auth-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === "admin" && password === "admin") {
        alert("Admin Sign In Successful!");
        // Redirect to the Admin Dashboard if credentials are correct
        window.location.href = "/admin/dashboard";  // Adjust path if needed
    } else if (username === "PK-01" && password === "pilot") {
        alert("Pilot Sign In Successful!");
        // Optionally add a redirect to the Pilot Dashboard if needed
        window.location.href = "/home";
    } else {
        alert("Invalid Username or Password");
    }
});
// document.getElementById('auth-form').addEventListener('submit', function(e) {
//     e.preventDefault();

//     const username = document.getElementById('username').value;
//     const password = document.getElementById('password').value;

//     if (username === "admin" && password === "admin") {
//         alert("Admin Sign In Successful!");
//         // Redirect to the Admin Dashboard if needed
//         window.location.href = "D:/Semester%203/SEC/VirtuFlight/Authenticate/Home/index.html";  // Adjust path if needed
//     } else if (username === "PK-01" && password === "pilot") {
//         alert("Pilot Sign In Successful!");
//         // Redirect to the home page for the pilot if credentials are correct
//         window.location.href = "home.html";  // Replace with the correct path to the home page
//     } else {
//         alert("Invalid Username or Password");
//     }
// });