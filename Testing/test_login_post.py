"""
This test case was created mostly by using a template from ChatGPT, which was then modified to work with this specific feature case
Before running any test, open a terminal and change the working directory to the project root (CS3300-Semester-Project) and run: pip install -r requirements.txt
Then, run the test by running (in the same open terminal): python -m unittest -v  Testing.testing
"""

import unittest
import sys
import os

# Add the parent directory to sys.path
# Not usually supposed to be done when working with Flask (accodsing to Flask's documentation, as __pycahce__ should be ignored, however was running into issues running tests)
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from flask import json


class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up a test client
        self.app = app.test_client()
        self.app.testing = True

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