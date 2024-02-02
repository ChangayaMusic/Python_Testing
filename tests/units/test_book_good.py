import unittest
from flask import Flask, get_flashed_messages
from server import app, loadClubs, loadCompetitions, saveClubs, saveCompetitions
from datetime import datetime, timedelta

class TestBooking(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the provided clubs JSON data for testing
        cls.mock_clubs = [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "12"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]

        # Save the mock clubs data to the file
        saveClubs(cls.mock_clubs)

        # Load the provided competitions JSON data for testing
        # Set competition dates to future dates
        future_date = datetime.now() + timedelta(days=30)

        cls.mock_competitions = [
            {"name": "Spring Festival", "date": future_date.strftime("%Y-%m-%d %H:%M:%S"), "numberOfPlaces": "25"},
            {"name": "Fall Classic", "date": (future_date + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"), "numberOfPlaces": "13"},
        ]

        # Save the mock competitions data to the file
        saveCompetitions(cls.mock_competitions)

    def setUp(self):
        self.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        # Clean up: Reset data files to their original state
        saveClubs([])
        saveCompetitions([])

    def test_purchase_places(self):
        # Mock the user input in the form
        form_data = {
            "competition": "Fall Classic",
            "club": "Simply Lift",
            "places": "1"
        }

        # Perform the request and capture the response
        with self.app as client:
            response = client.post("/purchasePlaces", data=form_data, follow_redirects=True)

        # Retrieve the updated mock data after the booking
        updated_clubs = loadClubs()
        updated_competitions = loadCompetitions()

        # Assert that the flash message indicates a successful booking
        self.assertIn(b"Great-booking complete!", response.data)

        # Assert that the points in the club have been updated
        self.assertEqual(updated_clubs[0]["points"], 11)

        # Assert that the number of places in the competition has been updated
        self.assertEqual(updated_competitions[1]["numberOfPlaces"], 12)

if __name__ == "__main__":
    unittest.main()
