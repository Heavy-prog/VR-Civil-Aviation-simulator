// Simulated user data for demonstration
const USER_DATA = {
    admin: { password: "admin", username: "Admin", lastSignIn: "Never" },
};

// Function to show popups
function showPopup(title, content) {
    const popupContainer = document.getElementById("popup-container");
    popupContainer.innerHTML = `
        <div class="popup">
            <h2>${title}</h2>
            <div class="popup-content">${content}</div>
            <button class="close-popup" onclick="closePopup()">Close</button>
        </div>
    `;
}

// Function to close popups
function closePopup() {
    console.log('Closing popup');
    document.getElementById("popup-container").innerHTML = "";
}

// Function to handle button clicks
function handleButtonClick(action) {
    console.log("Button clicked: " + action);  // Log the button action for debugging
    switch (action) {
        case 'Change Password':
            changePassword();
            break;
        case 'Add User':
            addUser();
            break;
        case 'Delete User':
            deleteUser();
            break;
        case 'View Users':
            viewUsers();
            break;
        case 'Log Out':
            logOut();
            break;
        default:
            break;
    }
}

// Function to change the password
function changePassword() {
    const content = `
        <label>Old Password:</label>
        <input type="password" id="old-password">
        <label>New Password:</label>
        <input type="password" id="new-password">
        <label>Confirm New Password:</label>
        <input type="password" id="confirm-password">
        <button onclick="savePassword()">Save</button>
    `;
    showPopup("Change Password", content);
}

// Function to save the new password
function savePassword() {
    const oldPassword = document.getElementById("old-password").value;
    const newPassword = document.getElementById("new-password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    if (USER_DATA.admin.password !== oldPassword) {
        alert("Old password is incorrect!");
        return;
    }
    if (newPassword !== confirmPassword) {
        alert("New passwords do not match!");
        return;
    }
    if (newPassword.length < 6) {
        alert("Password must be at least 6 characters long!");
        return;
    }

    USER_DATA.admin.password = newPassword;
    alert("Password changed successfully!");
    closePopup();
}

// Function to add a user
function addUser() {
    const content = `
        <label>Username:</label>
        <input type="text" id="new-username">
        <label>User ID:</label>
        <input type="text" id="new-user-id">
        <label>Password:</label>
        <input type="password" id="new-user-password">
        <button onclick="saveUser()">Add User</button>
    `;
    showPopup("Add User", content);
}

// Function to save the user
function saveUser() {
    const username = document.getElementById("new-username").value;
    const userId = document.getElementById("new-user-id").value;
    const password = document.getElementById("new-user-password").value;

    if (!username || !userId || !password) {
        alert("All fields are required!");
        return;
    }
    if (USER_DATA[userId]) {
        alert("User ID already exists!");
        return;
    }

    USER_DATA[userId] = { username, password, lastSignIn: "Never" };
    alert(`User '${username}' added successfully!`);
    closePopup();
}
document.querySelectorAll('.delete-user').forEach(button => {
    button.addEventListener('click', function () {
        const userId = this.dataset.id;

        fetch(`/delete-user/${userId}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                alert('User deleted successfully!');
                location.reload(); // Reload the page to refresh the user list
            } else {
                alert('Failed to delete user.');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

// Function to delete a user
// function deleteUser() {
//     const content = `
//         <label>User ID to Delete:</label>
//         <input type="text" id="delete-user-id">
//         <button onclick="performDelete()">Delete</button>
//     `;
//     showPopup("Delete User", content);
// }

// // Function to perform user deletion
// function performDelete() {
//     const userId = document.getElementById("delete-user-id").value;

//     if (!USER_DATA[userId]) {
//         alert("User ID not found!");
//         return;
//     }
//     if (userId === "admin") {
//         alert("Cannot delete admin!");
//         return;
//     }

//     delete USER_DATA[userId];
//     alert("User deleted successfully!");
//     closePopup();
// }

// Function to view users
function viewUsers() {
    let userList = "<ul>";
    for (const userId in USER_DATA) {
        const { username, lastSignIn } = USER_DATA[userId];
        userList += `<li><strong>${username}</strong> (ID: ${userId}, Last Sign-In: ${lastSignIn})</li>`;
    }
    userList += "</ul>";
    showPopup("User List", userList);
}

// Function to log out
function logOut() {
    alert("Logging out...");
    // Redirect to the sign-in page
    window.location.href = "D:/Semester%203/SEC/VirtuFlight/Authenticate/index.html"; // Replace this with your actual sign-in page URL
}
