document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.lab-form');
    const testMethodSelect = document.getElementById('test-method');
    const submitBtn = document.querySelector('.submit-btn');

    // Disable the submit button if no selection is made in the test method field
    form.addEventListener('submit', function(event) {
        if (testMethodSelect.value === "") {
            event.preventDefault(); // Prevent submission
            flash("Please select a test method.");
        }
    });

});


document.addEventListener('DOMContentLoaded', function() {
    const submitBtn = document.querySelector('.submit-btn');

    // Add ripple effect on click
    submitBtn.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const btnRect = submitBtn.getBoundingClientRect();
        const size = Math.max(btnRect.width, btnRect.height);
        const x = e.clientX - btnRect.left - size / 2;
        const y = e.clientY - btnRect.top - size / 2;

        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        ripple.classList.add('ripple');

        // Remove any previous ripples before adding a new one
        const previousRipple = submitBtn.querySelector('.ripple');
        if (previousRipple) {
            previousRipple.remove();
        }

        submitBtn.appendChild(ripple);

        // The ripple will automatically disappear due to CSS animations
    });
});


