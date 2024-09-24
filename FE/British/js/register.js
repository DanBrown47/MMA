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
        console.log("Sending form")
        console.log(formData)
        console.log("=======")
        fetch("http://127.0.0.1:9000/api/register/", {
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
