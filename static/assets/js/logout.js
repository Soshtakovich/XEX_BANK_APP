document.addEventListener('DOMContentLoaded', function () {
    // Add click event listener to the logout button
    document.getElementById('logoutBtn').addEventListener('click', function () {
        // Perform logout actions
        sessionStorage.removeItem('user_id'); // Clear the user ID from session storage
        sessionStorage.removeItem('user_name'); // Clear the user name from session storage (if needed)
        sessionStorage.removeItem('user_surname'); // Clear the user surname from session storage (if needed)

        // Redirect or perform any other logout operations as needed
        console.log('User logged out');
        // Example: Redirect to index.html
        window.location.href = "/index_2";
    });
});

