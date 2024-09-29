// Client-side validation for email, phone number, and username
const loginInput = document.getElementById('login_input');
const inputError = document.getElementById('inputError');

loginInput.addEventListener('input', function() {
    // Patterns for validation
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/; // Basic email pattern
    const phonePattern = /^\d{10}$/; // Assuming phone number is 10 digits
    const usernamePattern = /^[a-zA-Z0-9_.-]{3,20}$/; // Basic username pattern

    const inputValue = loginInput.value;

    if (emailPattern.test(inputValue) || phonePattern.test(inputValue) || usernamePattern.test(inputValue)) {
        inputError.style.display = 'none'; // Hide error message
    } else {
        inputError.style.display = 'block'; // Show error message
    }
});

// Prevent form submission if the input is invalid
document.getElementById("login-form").addEventListener("submit", function(event) {
    if (inputError.style.display === 'block') {
        alert("Please correct the errors before submitting the form.");
        event.preventDefault(); // Prevent form submission
    }
});