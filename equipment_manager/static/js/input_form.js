document.getElementById('equipment-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    const errorMessage = document.getElementById('error-message');
    errorMessage.style.display = 'none'; // Hide previous error messages

    // Get values from form
    const equipmentName = document.getElementById('equipment-name').value.trim();
    const equipmentID = document.getElementById('equipment_id')
    const imageUrlInput = document.getElementById('equipment-image');
    const managerName = document.getElementById('manager-name').value.trim();
    const managerEmail = document.getElementById('manager-email').value.trim();
    const managerContact = document.getElementById('manager-contact').value.trim();
    const managerDPInput = document.getElementById('manager-dp-input');
    const managerID = document.getElementById('manager_id')
    const description = document.getElementById('description').value.trim();
    const features = document.getElementById('features').value.trim().split('\t'); // Split by tab instead of comma

    // Validate required fields
    if (!equipmentName) {
        errorMessage.textContent = 'Equipment Name is required.';
    } else if (!imageUrlInput.files[0]) {
        errorMessage.textContent = 'Equipment Image is required.';
    } else if (!managerName) {
        errorMessage.textContent = 'Manager Name is required.';
    } else if (!managerID) {
        errorMessage.textContent = 'Manager ID is required.';
    } else if (!equipmentID) {
        errorMessage.textContent = 'Equipment ID is required.';
    } else if (!managerEmail) {
        errorMessage.textContent = 'Manager Email is required.';
    } else if (!managerContact) {
        errorMessage.textContent = 'Manager Email is required.';
    }else if (!managerDPInput.files[0]) {
        errorMessage.textContent = 'Manager DP is required.';
    } else if (!description) {
        errorMessage.textContent = 'Description is required.';
    } else if (!features[0]) {
        errorMessage.textContent = 'At least one feature is required.';
    } else {
        // All validations passed, process the form data
        // Update UI with entered data
        const cardTitle = document.getElementById('card-title');
        if (cardTitle) {
            cardTitle.textContent = equipmentName;
        }

        const managerNameCard = document.getElementById('manager-name-card');
        if (managerNameCard) {
            managerNameCard.textContent = managerName;
        }

        const managerEmailCard = document.getElementById('manager-email-card');
        if (managerEmailCard) {
            managerEmailCard.textContent = managerEmail;
        }

        const descriptionCard = document.getElementById('description-card');
        if (descriptionCard) {
            descriptionCard.textContent = description;
        }

        const featuresList = document.getElementById('features-list');
        if (featuresList) {
            featuresList.innerHTML = ''; // Clear previous features
            features.forEach(feature => {
                const li = document.createElement('li');
                li.textContent = feature.trim(); // Trim whitespace
                featuresList.appendChild(li);
            });
        }

        // If everything is valid, submit the form (uncomment the following line if you're ready to submit)
        // this.submit(); 
    }

    // Display the error message if any validation fails
    if (errorMessage.textContent) {
        errorMessage.style.display = 'block';
    }
});

// Update file upload labels
document.addEventListener('DOMContentLoaded', function() {
    const managerDpInput = document.getElementById('manager-dp-input');
    const managerLabel = document.getElementById('manager-dp-label');
    const equipmentImageInput = document.getElementById('equipment-image');
    const equipmentLabel = document.getElementById('equipment-image-label'); // Get the label for equipment image

    // Function to update the label text based on file input
    function updateLabelText(fileInput, label) {
        if (fileInput.files && fileInput.files.length > 0) {
            label.textContent = 'Chosen'; // Change label text to 'Chosen'
            label.style.color = 'green'; // Optional: Change label color to green
        } else {
            label.textContent = 'Choose File'; // Reset to default
            label.style.color = 'black'; // Reset color
        }
    }

    // Add event listeners for manager DP input
    if (managerDpInput && managerLabel) {
        managerDpInput.addEventListener('change', function() {
            updateLabelText(managerDpInput, managerLabel); // Update label for manager DP
        });
    }

    // Add event listeners for equipment image input
    if (equipmentImageInput && equipmentLabel) {
        equipmentImageInput.addEventListener('change', function() {
            updateLabelText(equipmentImageInput, equipmentLabel); // Update label for equipment image
        });
    }
});


document.getElementById('equipment-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this); // Create FormData from the form

    fetch('/submit_equipment_information', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            // Display error message
            document.getElementById('error-message').innerText = data.error;
            document.getElementById('error-message').style.display = 'block';
        } else {
            // Handle success (e.g., redirect or show success message)
            alert(data.message);
            window.location.reload(); // Reload the page or redirect
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('error-message').innerText = 'An error occurred.';
        document.getElementById('error-message').style.display = 'block';
    });
});