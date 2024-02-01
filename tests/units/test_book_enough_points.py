import unittest
from unittest.mock import patch
from flask import Flask, flash
from server import app, purchasePlaces, clubs, competitions

class BookPointsTest(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Propagate the exceptions to the test client
        self.app.testing = True

    @patch('server.clubs', [
        {"name": "Mocked Club", "email": "mocked@club.com", "points": "2"},
    ])
    @patch('server.competitions', [
        {"name": "Mocked Competition", "date": "2022-01-20 12:00:00", "numberOfPlaces": "5"},
    ])
    def test_purchase_places_not_enough_points(self):
        # Mocking the request form data
        with self.app as client:
            with client.session_transaction() as session:
                session['user_id'] = 'mocked@club.com'
            response = client.post('/purchasePlaces', data={'competition': 'Mocked Competition', 'club': 'Mocked Club', 'places': '5'})

        # Check if the flash message contains the expected text
        with app.test_request_context():
            self.assertIn(b"Not enough points", response.data)

if __name__ == '__main__':
    unittest.main()
