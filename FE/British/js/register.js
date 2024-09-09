document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log('Form submitted!');
        
        const formData = new FormData(form);
        
        // Add file inputs manually to ensure they're included
        const photoInput = document.getElementById('photo');
        const idProofInput = document.getElementById('id-proof');
        
        if (photoInput.files[0]) {
            formData.append('photo', photoInput.files[0]);
        }
        
        if (idProofInput.files[0]) {
            formData.append('id_proof', idProofInput.files[0]);
        }
        
        fetch('http://127.0.0.1:8000/api/register/', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Registration successful:', data);
            alert('Registration successful!');
            // Optionally, redirect the user or clear the form here
        })
        .catch(error => {
            console.error('Error during registration:', error);
            alert('Registration failed. Please try again.');
        });
    });
});