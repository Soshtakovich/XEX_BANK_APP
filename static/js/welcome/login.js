document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.querySelector("form[action='/login']");

    if (loginForm) {
        loginForm.addEventListener("submit", async function(event) {
            event.preventDefault();

            const formData = new FormData(loginForm);
            try {
                const response = await fetch("/login", {
                    method: "POST",
                    body: formData
                });

                if (response.ok) {
                    const responseData = await response.json();

                    if (responseData.error) {
                        alert(responseData.error); // Display error message from server
                    } else if (responseData.success) {
                        console.log("Login successful!");
                        sessionStorage.setItem('user_id', responseData.user_id); // Store user_id in sessionStorage
                        window.location.href = "/bank"; // Redirect to home page
                    } else {
                        console.log("Unexpected response:", responseData);
                        alert("An error occurred. Please try again later.");
                    }
                } else {
                    console.error("HTTP error " + response.status);
                    alert("An error occurred. Please try again later.");
                }
            } catch (error) {
                console.error("Fetch error:", error);
                alert("An error occurred. Please try again later.");
            }
        });
    } else {
        console.error("Login form not found.");
    }
});
