// Named function to handle saving a car
function saveCar(button, ids) {
    console.log("saveCar called");
    console.log("id being sent: ",button.id);
    console.log("array: ",ids);
    
    if (!ids.includes(button.id)){
        console.log("save");
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
                ids.append(number(button.id));
                button.textContent = 'Unsave';
                button.style.backgroundColor = 'lightgreen';
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

    else {
        console.log("unsave");
        fetch('/unsaveCar', {
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
                ids = ids.filter(num => num !== button.id);
                button.textContent = 'Save';
                button.style.backgroundColor = '#615b5b';
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

}

// Named function to handle unsaving a car
function unsaveCar(button) {
    console.log("unsaveCar function called");
    button.textContent = 'Save';

    // Remove the unsave handler and add the save handler
    button.removeEventListener('click', button.unsaveHandler);
    button.addEventListener('click', button.saveHandler);
}