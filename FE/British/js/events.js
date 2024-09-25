const eventContainer = document.getElementById("eventContainer");

function createEventCard(event) {
  const eventCard = document.createElement("div");
  eventCard.classList.add("event-card");

  const eventTitle = document.createElement("h2");
  eventTitle.classList.add("event-title");
  eventTitle.textContent = event.event_name;
  eventCard.appendChild(eventTitle);

  const eventDescription = document.createElement("p");
  eventDescription.classList.add("event-description");
  eventDescription.textContent = event.description;
  eventCard.appendChild(eventDescription);

  const eventDetails = document.createElement("div");
  eventDetails.classList.add("event-details");
  eventDetails.innerHTML = `
    <p><strong>Event Type:</strong> ${event.event_type.type}</p>
    <p><strong>Date:</strong> ${event.date}</p>
    <p><strong>Time:</strong> ${event.time}</p>
    <p><strong>Location:</strong> ${event.location}</p>
    <p><strong>Max Participants:</strong> ${event.max_participants}</p>
    <p><strong>Organizer:</strong> ${event.organizer_name}</p>
  `;
  eventCard.appendChild(eventDetails);

  const eventFees = document.createElement("p");
  eventFees.classList.add("event-fees");
  eventFees.textContent = `Fees: $${event.fees}`;
  eventCard.appendChild(eventFees);

  const expandedCard = createExpandedEventCard(event);
  expandedCard.classList.add("hidden");

  eventCard.addEventListener("click", () => {
    expandedCard.classList.toggle("hidden");
  });

  const container = document.createElement("div");
  container.appendChild(eventCard);
  container.appendChild(expandedCard);

  return container;
}

function createExpandedEventCard(event) {
  const eventCard = document.createElement("div");
  eventCard.classList.add("expanded-event-card");

  const eventCardContent = document.createElement("div");
  eventCardContent.classList.add("event-card-content");

  const eventTitle = document.createElement("h2");
  eventTitle.classList.add("event-title");
  eventTitle.textContent = event.event_name;
  eventCardContent.appendChild(eventTitle);

  const eventDescription = document.createElement("p");
  eventDescription.classList.add("event-description");
  eventDescription.textContent = event.description;
  eventCardContent.appendChild(eventDescription);

  const eventDetails = document.createElement("div");
  eventDetails.classList.add("event-details");
  eventDetails.innerHTML = `
    <p><strong>Event Type:</strong> ${event.event_type.type}</p>
    <p><strong>Date:</strong> ${event.date}</p>
    <p><strong>Time:</strong> ${event.time}</p>
    <p><strong>Location:</strong> ${event.location}</p>
    <p><strong>Max Participants:</strong> ${event.max_participants}</p>
    <p><strong>Organizer:</strong> ${event.organizer_name}</p>
  `;
  eventCardContent.appendChild(eventDetails);

  const eventFees = document.createElement("p");
  eventFees.classList.add("event-fees");
  eventFees.textContent = `Fees: $${event.fees}`;
  eventCardContent.appendChild(eventFees);

  const expandedContent = document.createElement("div");
  expandedContent.classList.add("expanded-content");

  const qrCodeDiv = document.createElement("div");
  qrCodeDiv.classList.add("qr-code");
  const qrCodeInput = document.createElement("input");
  qrCodeInput.type = "file";
  qrCodeInput.addEventListener("change", handleQrCodeUpload);
  qrCodeDiv.appendChild(qrCodeInput);
  expandedContent.appendChild(qrCodeDiv);

  const screenshotDiv = document.createElement("div");
  screenshotDiv.classList.add("screenshot");
  const screenshotInput = document.createElement("input");
  screenshotInput.type = "file";
  screenshotInput.addEventListener("change", handleScreenshotUpload);
  const igniteButton = document.createElement("button");
  igniteButton.classList.add("ignite-button", "disabled");
  igniteButton.textContent = "Ignite";
  igniteButton.addEventListener("click", handleIgnite);
  screenshotDiv.appendChild(screenshotInput);
  screenshotDiv.appendChild(igniteButton);
  expandedContent.appendChild(screenshotDiv);

  eventCard.appendChild(eventCardContent);
  eventCard.appendChild(expandedContent);

  return eventCard;
}

let qrCodeImage = null;
let screenshotImage = null;

function handleQrCodeUpload(e) {
  qrCodeImage = e.target.files[0];
}

function handleScreenshotUpload(e) {
  screenshotImage = e.target.files[0];
  const igniteButton = e.target.parentNode.querySelector(".ignite-button");
  igniteButton.classList.remove("disabled");
}

function handleIgnite() {
  // Add your logic to handle the "Ignite" button click
  console.log("Ignite button clicked!");
}

fetch(apiUrl)
  .then(response => response.json())
  .then(events => {
    events.forEach(event => {
      const eventContainer = createEventCard(event);
      this.eventContainer.appendChild(eventContainer);
    });
  })
  .catch(error => {
    console.error("Error fetching events:", error);
  });e.error("Error fetching events:", error);
  });