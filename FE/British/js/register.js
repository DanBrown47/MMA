// document.addEventListener('DOMContentLoaded', function() {
//     const form = document.querySelector('form');
    
//     form.addEventListener('submit', function(e) {
//         e.preventDefault();
//         console.log('Form submitted!');
        
//         const formData = new FormData(form);
        
//         // Add file inputs manually to ensure they're included
//         const photoInput = document.getElementById('photo');
//         const idProofInput = document.getElementById('id-proof');
        
//         if (photoInput.files[0]) {
//             formData.append('photo', photoInput.files[0]);
//         }
        
//         if (idProofInput.files[0]) {
//             formData.append('id_proof', idProofInput.files[0]);
//         }
//         //mamtha
//         // Fetch the CSRF token from the cookie
//         const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)[1];
//         //mamtha
//         fetch('http://127.0.0.1:8000/api/register/', {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-CSRFToken': csrfToken // Include the CSRF token in headers
//             }
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             console.log('Registration successful:', data);
//             alert('Registration successful!');
//             // Optionally, redirect the user or clear the form here
//             window.location.href = '/success-page/'; // Redirect to a success page
//         })
//         .catch(error => {
//             console.error('Error during registration:', error);
//             alert('Registration failed. Please try again.');
//         });
//     });
// });
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    
    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent the form from submitting the default way
        console.log('success');
        // Create a FormData object to handle file uploads and form data
        const formData = new FormData(form);

        // Send the POST request using Fetch API
        fetch("http://127.0.0.1:8000/api/register/", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // Handle the response data here
            console.log("Success:", data);
            alert("Registration successful!");
        })
        .catch(error => {
            console.error("Error:", error);
            alert("There was an error with the registration. Please try again.");
        });
    });
});
