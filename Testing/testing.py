# These test cases were created mostly by using a template from ChatGPT, which was then modified to qwork qith our specific feature cases
# Before running any tests, open a terminal and change the working dircetory to the project root (where app.py is located) and run: pip install -r requirements.txt
# Then, run these test by running (in the same open terminal): python -m unittest -v  Testing.testing


import unittest
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from flask import json


class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up a test client
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        # Perform a GET request to the home page
        response = self.app.get('/')
        # Assert that the status code is 200
        self.assertEqual(response.status_code, 200)
        # Assert that the rendered page contains specific content
        self.assertIn(b'<h2>Vehicle Price Estimator</h2>', response.data)

    def test_buy_page(self):
        # Test the buy page
        response = self.app.get('/buy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'minMilesDrop', response.data)  # Replace with actual content on the buy page

    def test_sell_page(self):
        # Test the sell page
        response = self.app.get('/sell')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Sell</title>', response.data)  # Replace with actual content on the sell page

    def test_contact_page(self):
        # Test the contact page
        response = self.app.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Contact Us</title>', response.data)  # Replace with actual content on the contact page

    def test_about_page(self):
        # Test the about page
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>About</title>', response.data)  # Replace with actual content on the about page

    def test_price_prediction_post_request(self):
        # Test the /price_prediction endpoint with a POST request
        data = {
            'vin': '1FTEW1EP4JKE30880',
            'miles1': '15000',
            'year': '',  # Empty strings instead of None for form submission
            'make': '',
            'model': '',
            'trim': '',
            'miles2': '',
        }
        response = self.app.post('/price_prediction', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # print(response.data.decode())

        # Check if the "Details" section is present in the response
        self.assertIn(b'<p>Details:</p>', response.data)

        # # You can also check for specific elements like the modal content
        # self.assertIn(b'Predicted Price:', response.data)
        # self.assertIn(b'Make:', response.data)
        # self.assertIn(b'Model:', response.data)
        # self.assertIn(b'Year:', response.data)
        # self.assertIn(b'Trim:', response.data)


    def test_invalid_price_prediction(self):
        # Test the /price_prediction endpoint with invalid data
        data = {
            'vin': None,
            'miles1': None,
            'year': '1960',  # Invalid year
            'make': 'Toyota',
            'model': 'Camry',
            'trim': 'LE',
            'miles2': '10000',
        }
        response = self.app.post('/price_prediction', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error: Failed to retrieve prediction.', response.data)  # Replace with error message content

    def test_register_page(self):
        # Test the register page
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data)  # Replace with actual content on the register page

    def test_login_post_request(self):
        # Test the login endpoint with a POST request
        data = json.dumps({'username': 'testuser', 'password': 'testpassword'})
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/login', data=data, headers=headers)
        # Check for appropriate response
        self.assertIn(response.status_code, [200, 401])  # Expecting either success or failure
        if response.status_code == 200:
            self.assertIn(b'Login successful!', response.data)
        else:
            self.assertIn(b'Error:', response.data)

    def test_invalid_route(self):
        # Test a route that does not exist
        response = self.app.get('/non_existent_route')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 Not Found', response.data)

if __name__ == '__main__':
    unittest.main()