//Get id numbers of saved cars
function getSavedCars() {
    const token = localStorage.getItem("access_token");
    if (!token) return Promise.resolve([]);

    return fetch('/getSavedCars', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token: token })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.isValid) {
            console.log("Array in getSavedCars:", data.carIdArray);
            return data.carIdArray; // Explicitly return the carIdArray
        } else {
            console.error("getSavedCars: Invalid data returned from server.");
            return []; // Return an empty array for invalid responses
        }
    })
    .catch(error => {
        console.error('Error during getSavedCars:', error);
        return []; // Return an empty array if there’s an error
    });
}