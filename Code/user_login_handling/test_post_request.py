#This file is only for POST request testing, this is not part of the final project

import requests
import json

# URL of Flask app running locally
url = 'http://127.0.0.1:5000/login'

# Sample JSON data to send in the request
payload = {
    "username": "testuser",
    "password": "password123"
}

# Send a POST request with the JSON data
response = requests.post(url, json=payload)

# Print out the response content
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.json())