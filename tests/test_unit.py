import unittest
from datetime import datetime, timedelta
from server import app


class TestBooking(unittest.TestCase):
    def setUp(self):
        # Set up your test data, including clubs and competitions
        self.clubs = [
            {
                "name": "Simply Lift",
                "email": "john@simplylift.co",
                "points": "13"
            },
            {
                "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4"
            },
            {
                "name": "She Lifts",
                "email": "kate@shelifts.co.uk",
                "points": "12"
            }
        ]

        self.competitions = [
            {
                "name": "Spring Festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25"
            },
            {
                "name": "Fall Classic",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "13"
            }
        ]

    def test_booking_past_competition(self):
        # Choose a past competition for testing
        past_competition = {'name': 'Spring Festival', 'date': '2020-03-27 10:00:00'}
        self.competitions.append(past_competition)

        # Simulate a request to the book route for the past competition
        with app.test_client() as client:
            response = client.get('/book/Spring Festival/Simply Lift')

            # Check if the flash message is displayed
            self.assertIn(b"Error: Competition date is in the past", response.data)

