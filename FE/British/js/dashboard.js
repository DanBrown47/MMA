function fetchDataofUser() {
    const access_token = localStorage.getItem('token');
    console.log(access_token);
    
    fetch('http://127.0.0.1:8000/dashboard', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`  // Add 'Bearer ' before the token
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.profile) {
            console.log(data);
            const profile_pic_url = data.profile.photo;  // Declare variables
            const name_of_fighter = data.profile.name;
            const age_of_fighter = data.profile.age;

            document.getElementById('name_of_fighter').innerText = name_of_fighter;
            document.getElementById('age_of_fighter').innerText = age_of_fighter;
            // Set other elements if needed
        } else {
            document.getElementById('konakona').textContent = "Backend is facing fever";
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        document.getElementById('konakona').textContent = "An error occurred while fetching data.";
    });
}

function logout(){
    localStorage.clear()
    window.location.href = '/FE/British/src/login.html';
}

window.onload = function() {
    fetchDataofUser();
};
