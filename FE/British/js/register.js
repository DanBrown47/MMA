
// document.addEventListener("DOMContentLoaded", function() {
//     const form = document.querySelector("form");
    
//     form.addEventListener("submit", function(event) {
//         event.preventDefault(); // Prevent the form from submitting the default way
//         console.log('success');
//         // Create a FormData object to handle file uploads and form data
//         const formData = new FormData(form);

//         // Send the POST request using Fetch API
//         fetch("http://127.0.0.1:8000/api/register/", {
//             method: "POST",
//             body: formData,
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok ' + response.statusText);
//             }
//             return response.json();
//         })
//         .then(data => {
//             // Handle the response data here
//             console.log("Success:", data);
//             alert("Registration successful!");
//         })
//         .catch(error => {
//             console.error("Error:", error);
//             alert("There was an error with the registration. Please try again.");
//         });
//     });
// });
// document.addEventListener("DOMContentLoaded", function() {
//     const dobInput = document.getElementById('date_of_birth'); 
//     const ageInput = document.getElementById('age');  
//     const form = document.querySelector("form");  

//     // Event listener to calculate age when DOB is changed
//     dobInput.addEventListener('change', function() {
//         const dobValue = this.value;
//         console.log("Selected DOB:", dobValue);  // Log DOB

//         if (dobValue) {
//             const dob = new Date(dobValue);
//             const today = new Date();
//             let age = today.getFullYear() - dob.getFullYear();
//             const monthDiff = today.getMonth() - dob.getMonth();

//             // Adjust age if needed
//             if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
//                 age--;
//             }

//             // Set the age field value
//             ageInput.value = age;
//             console.log("Calculated Age:", age);  // Log calculated age
//         }
//     });

//     // Form submission with age calculation
//     form.addEventListener("submit", function(event) {
//         event.preventDefault();  // Prevent default form submission
//         console.log('Form Submitted');
        
//         // Ensure age is calculated before submission (Optional but recommended)
//         if (!ageInput.value) {
//             alert("Please select Date of Birth to calculate age.");
//             return;  // Do not submit if age is not calculated
//         }

//         // Create FormData object
//         const formData = new FormData(form);

//         // Submit form data using Fetch API
//         fetch("http://127.0.0.1:8000/api/register/", {
//             method: "POST",
//             body: formData,
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok ' + response.statusText);
//             }
//             return response.json();
//         })
//         .then(data => {
//             console.log("Success:", data);  // Log success response
//             alert("Registration successful!");
//         })
//         .catch(error => {
//             console.error("Error:", error);  // Log error response
//             alert("There was an error with the registration. Please try again.");
//         });
//     });
// });
document.addEventListener("DOMContentLoaded", function() {
    const dobInput = document.getElementById('date_of_birth'); 
    const ageInput = document.getElementById('age');  
    const weightInput = document.getElementById('weight'); 
    const weightCategoryInput = document.getElementById('weight_category');  
    const form = document.querySelector("form");  

    // Weight categories in kg
    const weightCategoriesKg = [
        { name: 'Strawweight', limit: 52.2 },
        { name: 'Flyweight', limit: 56.7 },
        { name: 'Bantamweight', limit: 61.2 },
        { name: 'Featherweight', limit: 65.8 },
        { name: 'Lightweight', limit: 70.3 },
        { name: 'Super lightweight', limit: 74.8 },
        { name: 'Welterweight', limit: 77.1 },
        { name: 'Super welterweight', limit: 79.4 },
        { name: 'Middleweight', limit: 83.9 },
        { name: 'Super middleweight', limit: 88.5 },
        { name: 'Light heavyweight', limit: 93.0 },
        { name: 'Cruiserweight', limit: 102.1 },
        { name: 'Heavyweight', limit: 120.2 },
        { name: 'Super heavyweight', limit: Infinity }  
    ];

    // Function to determine weight category based on weight in kg
    function getWeightCategoryKg(weight) {
        for (let category of weightCategoriesKg) {
            if (weight <= category.limit) {
                return category.name;
            }
        }
        return "Unknown";
    }

    // Event listener to calculate age when DOB is changed
    dobInput.addEventListener('change', function() {
        const dobValue = this.value;
        if (dobValue) {
            const dob = new Date(dobValue);
            const today = new Date();
            let age = today.getFullYear() - dob.getFullYear();
            const monthDiff = today.getMonth() - dob.getMonth();
            if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
                age--;
            }
            ageInput.value = age;
        }
    });

    // Event listener to calculate weight category when weight is entered (in kg)
    weightInput.addEventListener('input', function() {
        const weightValue = parseFloat(this.value);
        if (weightValue) {
            const weightCategory = getWeightCategoryKg(weightValue);
            weightCategoryInput.value = weightCategory;
        } else {
            weightCategoryInput.value = "";
        }
    });

    // Form submission with age and weight category calculation
    form.addEventListener("submit", function(event) {
        event.preventDefault();  
        
        // Ensure age is calculated
        if (!ageInput.value) {
            alert("Please select Date of Birth to calculate age.");
            return;
        }

        // Ensure weight category is filled
        if (!weightCategoryInput.value) {
            alert("Please enter a valid weight to determine the weight category.");
            return;
        }

        const formData = new FormData(form);

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
            alert("Registration successful!");
        })
        .catch(error => {
            console.error("Error:", error);
            alert("There was an error with the registration. Please try again.");
        });
    });
});
