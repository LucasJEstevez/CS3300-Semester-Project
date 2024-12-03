// Named function to handle saving a car
function saveCar() {
    console.log("id being sent: ",saveButton.id);
    
    console.log("In saveCar, savedVehicleIds:",savedVehicleIds);
    fetch('/saveCar', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({token: token,"id":button.id})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        if (data.success) {

            button.textContent = 'Unsave';
            button.style.backgroundColor = 'lightgreen';

            // You need to pass the same reference for removeEventListener
            button.removeEventListener('click', button.saveHandler);
            
            // Add the new event listener for "Unsave"
            button.addEventListener('click', button.unsaveHandler);
        }
        else{
            if (data.message == "User not logged in") {
                window.location.href = "/sign-in";
            }
        }
    })
    .catch(error => {
        console.error('Error during request:', error);
        console.error('Request failed: ' + error.message);
    });
}

// Named function to handle unsaving a car
function unsaveCar(button) {
    console.log("unsaveCar function called");
    button.textContent = 'Save';

    // Remove the unsave handler and add the save handler
    button.removeEventListener('click', button.unsaveHandler);
    button.addEventListener('click', button.saveHandler);
}