document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript is working!');
});

document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript is working!');
});

function toggleForms() {
    const loginSection = document.getElementById('login-section');
    const signinSection = document.getElementById('signin-section');

    // Toggle visibility
    if (loginSection.style.display === 'none') {
        loginSection.style.display = 'block';
        signinSection.style.display = 'none';
    } else {
        loginSection.style.display = 'none';
        signinSection.style.display = 'block';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript is working!'); // For debugging
});

// Function to show content after successful login or signup
function showContent(username) {
    const loginSection = document.getElementById('login-section');
    const signinSection = document.getElementById('signin-section');
    const contentSection = document.getElementById('content-section');

    loginSection.style.display = 'none';
    signinSection.style.display = 'none';
    contentSection.style.display = 'block';
    document.querySelector("#content-section h1").textContent = `Welcome, ${username}!`;
}

// Example success logic after login or signup
function onLoginSuccess(username) {
    showContent(username);
}

function onSigninSuccess(username) {
    showContent(username);
}


//togle action

function toggleDiv(divId) {
    var element = document.getElementById(divId);

    // Toggle the 'active' class on the clicked div
    if (element.classList.contains('active')) {
        element.classList.remove('active');
    } else {
        element.classList.add('active');
    }
}