//If the user is not logged into a page that requires a login, they will be redirected to the sign-in page

const token = localStorage.getItem("access_token");
let loggedIn = false;
console.log("Token (if=false):",token);

if (token) {
    console.log('Token (if=true):', token);
    fetch('/isValidToken', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ token: token }) // Convert body to JSON string
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        if (data.isValid) {

            window.location.href = "/saved-cars";
        }
    })
    .catch(error => {
        console.error('Error during request:', error);
        document.getElementById("welcome_header").innerHTML = 'Request failed: ' + error.message;
    });
}