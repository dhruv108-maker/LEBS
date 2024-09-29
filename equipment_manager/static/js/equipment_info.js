document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript is working!');
});

function openInputPage() {
    const equipmentCardContainer = document.getElementById('equipment-card-container');
    const inputFormContainer = document.getElementById('input-form-container');

    // Hide the equipment card and show the input form with smooth transitions
    equipmentCardContainer.style.display = 'none';
    inputFormContainer.style.display = 'flex';
    inputFormContainer.style.justifyContent = 'center';
    inputFormContainer.style.width = '100%';
    
    // Optional: Add smooth transitions by changing opacity
    inputFormContainer.style.opacity = 0;
    setTimeout(() => {
        inputFormContainer.style.transition = 'opacity 0.5s ease';
        inputFormContainer.style.opacity = 1;
    }, 10);  // Delay for ensuring the transition takes effect
}

