// Named function to handle saving a car
function saveCar(button) {
    console.log("saveCar function called");
    button.textContent = 'Unsave';

    // You need to pass the same reference for removeEventListener
    button.removeEventListener('click', saveHandler(button));
    
    // Add the new event listener for "Unsave"
    button.addEventListener('click', unsaveHandler(button));
}

// Function that acts as a handler for the "Save" button
function saveHandler(button) {
    return function () {
        saveCar(button);
    };
}

// Named function to handle unsaving a car
function unsaveCar(button) {
    console.log("unsaveCar function called");
    button.textContent = 'Save';

    // You need to pass the same reference for removeEventListener
    button.removeEventListener('click', unsaveHandler(button));

    // Add the new event listener for "Save"
    button.addEventListener('click', saveHandler(button));
}

// Function that acts as a handler for the "Unsave" button
function unsaveHandler(button) {
    return function () {
        unsaveCar(button);
    };
}