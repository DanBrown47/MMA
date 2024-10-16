
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
            document.getElementById('unique_id').innerText = data.profile.unique_id;
            document.getElementById('name_of_fighter').innerText = data.profile.name;
            document.getElementById('age_of_fighter').innerText = data.profile.age;
            document.getElementById('weight_of_fighter').innerText = data.profile.weight;
            document.getElementById('weight_category').innerText = data.profile.weight_category;
            document.getElementById('height_of_fighter').innerText = data.profile.height;
            document.getElementById('club_of_fighter').innerText = data.profile.club_name;
            document.getElementById('coach_name').innerText = data.profile.coach_name;
            
        }
    })
    .catch(error => console.error('Error fetching profile data:', error));
}
