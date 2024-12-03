"""
This test case was created mostly by using a template from ChatGPT, which was then modified to work with this specific feature case. In this case we are testing
not only the speed of our price predictor (test result output includes time to execute test, therefore testing non-functional req of <5 second prediction), but
also the case of handling invalid input (missing data, specifically with vin method of estimation). Test will run with "OK" as output if the POST request is 
handled and failure message is returned.
Before running any test, add the API key you were given by MarketCheck into line 86 of app.py; this will allow you to run price predictor tests. Ensure you replace this with the original
code when done testing. Next, open a terminal and change the working directory to the project root (CS3300-Semester-Project) and run: pip install -r requirements.txt
Then, run the test by running (in the same open terminal): python -m unittest -v  Testing.test_pp_vin_missing_data
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

    def test_invalid_price_prediction_vin_missing_data(self):
        # Test the /price_prediction endpoint with invalid data
        data = {
            'vin': '1FTEW1EP4JKE30880',
            'miles1': '', # Missing miles
            'year': '',  
            'make': '',
            'model': '',
            'trim': '',
            'miles2': '',
        }
        response = self.app.post('/price_prediction', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error: Failed to retrieve prediction.', response.data)