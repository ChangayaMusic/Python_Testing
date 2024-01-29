import unittest
from unittest.mock import patch
from flask import Flask, flash
from server import app, purchasePlaces, clubs, competitions

class BookMoreThan12PointsTest(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Propagate the exceptions to the test client
        self.app.testing = True

    @patch('server.clubs', [
        {"name": "Mocked Club", "email": "mocked@club.com", "points": "20"},
    ])
    @patch('server.competitions', [
        {"name": "Mocked Competition", "date": "2022-01-20 12:00:00", "numberOfPlaces": "20"},
    ])
    def test_purchase_places_12_places(self):
        # Mocking the request form data
        with self.app as client:
            with client.session_transaction() as session:
                session['user_id'] = 'mocked@club.com'
            response = client.post('/purchasePlaces', data={'competition': 'Mocked Competition', 'club': 'Mocked Club', 'places': '20'})

        # Check if the flash message contains the expected text
        with app.test_request_context():
            self.assertIn(b"Error: Can&#39;t book more than 12 places", response.data)

if __name__ == '__main__':
    unittest.main()
