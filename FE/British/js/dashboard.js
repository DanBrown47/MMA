// function fetchDataofUser() {
//     const access_token = localStorage.getItem('token');
//     console.log(access_token);
    
//     fetch('http://127.0.0.1:8000/dashboard', {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/json',
//             'Authorization': `Bearer ${access_token}`  // Add 'Bearer ' before the token
//         }
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         return response.json();
//     })
//     .then(data => {
//         if (data.profile) {
//             console.log(data);
//             const profile_pic_url = data.profile.photo;  // Declare variables
//             const name_of_fighter = data.profile.name;
//             const age_of_fighter = data.profile.age;
//             const weight_of_fighter=data.profile.weight;
//             const height_of_fighter=data.profile.height;
//             const club_of_fighter=data.profile.club_name;


//             document.getElementById('name_of_fighter').innerText = name_of_fighter;
//             document.getElementById('age_of_fighter').innerText = age_of_fighter;
//             document.getElementById('weight_of_fighter').innerText = weight_of_fighter;
//             document.getElementById('height_of_fighter').innerText = height_of_fighter;
//             document.getElementById('club_of_fighter').innerText = club_of_fighter;
            
//             // Set other elements if needed
//         } else {
//             document.getElementById('konakona').textContent = "Backend is facing fever";
//         }
//     })
//     .catch(error => {
//         console.error('Error fetching data:', error);
//         document.getElementById('konakona').textContent = "An error occurred while fetching data.";
//     });
// }

// function logout(){
//     localStorage.clear()
//     window.location.href = '/FE/British/src/login.html';
// }

// window.onload = function() {
//     fetchDataofUser();
// };
document.getElementById('show_profile').addEventListener('click', function() {
    document.getElementById('profile_section').classList.add('active');
    document.getElementById('event_section').classList.remove('active');
});

document.getElementById('show_events').addEventListener('click', function() {
    document.getElementById('profile_section').classList.remove('active');
    document.getElementById('event_section').classList.add('active');
    fetchEventDetails();
});

function fetchEventDetails() {
    const access_token = localStorage.getItem('token');
    fetch('http://127.0.0.1:8000/dashboard/events', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.events) {
            const event = data.events[0]; // For now, taking the first event. You can loop through for multiple.
            document.getElementById('event_name').innerText = event.name;
            document.getElementById('event_date').innerText = event.date;
            document.getElementById('event_location').innerText = event.location;
            document.getElementById('event_eligibility').innerText = event.eligibility;
            document.getElementById('event_rules').innerText = event.rules;
        }
    })
    .catch(error => console.error('Error fetching event details:', error));
}

function logout(){
    localStorage.clear();
    window.location.href = '/FE/British/src/login.html';
}

window.onload = function() {
    fetchProfileData();
};

function fetchProfileData() {
    const access_token = localStorage.getItem('token');
    fetch('http://127.0.0.1:8000/dashboard', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.profile) {
            document.getElementById('profile_pic').src = data.profile.photo;
            document.getElementById('profile_name').innerText = data.profile.name;
            document.getElementById('name_of_fighter').innerText = data.profile.name;
            document.getElementById('age_of_fighter').innerText = data.profile.age;
            document.getElementById('weight_of_fighter').innerText = data.profile.weight;
            document.getElementById('height_of_fighter').innerText = data.profile.height;
            document.getElementById('club_of_fighter').innerText = data.profile.club_name;
        }
    })
    .catch(error => console.error('Error fetching profile data:', error));
}
