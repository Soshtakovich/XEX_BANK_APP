document.addEventListener("DOMContentLoaded", function() {
    const signupForm = document.querySelector("form[action='/signup']");

    if (signupForm) {
        signupForm.addEventListener("submit", async function(event) {
            event.preventDefault();

            const formData = new FormData(signupForm);
            try {
                const response = await fetch("/signup", {
                    method: "POST",
                    body: formData
                });

                if (response.ok) {
                    const responseData = await response.json();

                    if (responseData.error) {
                        alert(responseData.error); 
                    } else if (responseData.success) {
                        console.log("Signup successful!");
                        alert("Signup successful! You can now log in.");
                        window.location.href = "/login"; 
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
        console.error("Signup form not found.");
    }
});
