"""
This test case was created mostly by using a template from ChatGPT, which was then modified to work with this specific feature case. In this case, we are testing the
functionality of our buy page by ensuring the "minMilesDrop" filter button is displayed on the page. Test will run with "OK" as output if the buy page (filters) is rendered correctly.
Before running any test, open a terminal and change the working directory to the project root (CS3300-Semester-Project) and run: pip install -r requirements.txt
Then, run the test by running (in the same open terminal): python -m unittest -v  Testing.test_buy
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

    def test_buy_page(self):
        # Test the buy page
        response = self.app.get('/buy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'minMilesDrop', response.data)