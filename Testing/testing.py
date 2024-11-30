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
        # Replace 'Welcome to the Home Page' with actual content in your index.html
        self.assertIn(b'<h2>Vehicle Price Estimator</h2>', response.data)

if __name__ == '__main__':
    unittest.main()