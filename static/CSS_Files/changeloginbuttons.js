const token = localStorage.getItem("access_token");
let loggedIn = false;

if (token) {
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
            loggedIn = true;

            var signin_button = document.getElementById("sign-in_button");
            signin_button.innerHTML = 'Saved Cars';
            signin_button.href = "/saved-cars";

            var register_button = document.getElementById("register_button");
            register_button.innerHTML = 'Sign Out';
            register_button.removeAttribute('href');
            register_button.onclick = signOut;
        }
    })
    .catch(error => {
        console.error('Error during request:', error);
        document.getElementById("welcome_header").innerHTML = 'Request failed: ' + error.message;
    });
}

function signOut(){
    localStorage.removeItem("access_token");
    window.location.href = "/";
}