const apiUrl = "http://127.0.0.1:9000/dashboard/events/";
const eventContainer = document.getElementById("eventContainer");
const eventModal = document.getElementById("eventModal");
const eventModalTitle = document.getElementById("eventModalTitle");
const eventModalDescription = document.getElementById("eventModalDescription");
const eventModalDetails = document.getElementById("eventModalDetails");
const eventModalClose = document.getElementById("eventModalClose");

eventModalClose.addEventListener("click", () => {
    eventModal.classList.remove("active");
});

fetch(apiUrl)
    .then(response => response.json())
    .then(events => {
        events.forEach(event => {
            const eventCard = document.createElement("div");
            eventCard.classList.add("event-card");
            eventCard.dataset.eventId = event.id;

            const eventTitle = document.createElement("h2");
            eventTitle.classList.add("event-title");
            eventTitle.textContent = event.event_name;
            eventCard.appendChild(eventTitle);

            const eventDescription = document.createElement("p");
            eventDescription.classList.add("event-description");
            eventDescription.textContent = event.description;
            eventCard.appendChild(eventDescription);

            const eventFees = document.createElement("p");
            eventFees.classList.add("event-fees");
            eventFees.textContent = `Fees: $${event.fees}`;
            eventCard.appendChild(eventFees);

            eventCard.addEventListener("click", () => {
                const eventId = eventCard.dataset.eventId;
                fetch(`http://127.0.0.1:9000/dashboard/events/${eventId}/`)
                    .then(response => response.json())
                    .then(eventDetails => {
                        eventModalTitle.textContent = eventDetails.event_name;
                        eventModalDescription.textContent = eventDetails.description;
                        eventModalDetails.innerHTML = `
                            <p><strong>Event Type:</strong> ${eventDetails.event_type}</p>
                            <p><strong>Date:</strong> ${eventDetails.date}</p>
                            <p><strong>Time:</strong> ${eventDetails.time}</p>
                            <p><strong>Location:</strong> ${eventDetails.location}</p>
                            <p><strong>Max Participants:</strong> ${eventDetails.max_participants}</p>
                            <p><strong>Organizer:</strong> ${eventDetails.organizer_name}</p>
                            <p><strong>Fees:</strong> $${eventDetails.fees}</p>
                        `;
                        eventModal.classList.add("active");
                    })
                    .catch(error => {
                        console.error("Error fetching event details:", error);
                    });
            });

            eventContainer.appendChild(eventCard);
        });
    })
    .catch(error => {
        console.error("Error fetching events:", error);
    });
