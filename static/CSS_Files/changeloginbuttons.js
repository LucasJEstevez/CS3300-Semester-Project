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
            loggedIn = true;

            var signin_button = document.getElementById("sign-in_button");
            signin_button.innerHTML = 'Saved Cars';
            signin_button.href="{{ url_for('saved_cars_page') }}";

            var register_button = document.getElementById("register_button");
            register_button.innerHTML = 'Sign Out';
            register_button.removeAttribute('href');
            register_button.onclick = signOut;
        } else {
            document.getElementById("welcome_header").innerHTML = 'Invalid token or user not found.';
        }
    })
    .catch(error => {
        console.error('Error during request:', error);
        document.getElementById("welcome_header").innerHTML = 'Request failed: ' + error.message;
    });
}

function signOut(){
    localStorage.removeItem("access_token");
    location.reload();
}