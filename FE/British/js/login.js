document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('http://127.0.0.1:8000/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            
        },
        body: JSON.stringify({ email: email, password: password  })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem('token', data.access);  // Store JWT token
            window.location.href = '/FE/British/src/dashboard.html';  // Redirect to dashboard
        } else {
            document.getElementById('error-message').textContent = 'Invalid credentials. Please try again.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('error-message').textContent = 'An error occurred. Please try again later.';
    });
});

