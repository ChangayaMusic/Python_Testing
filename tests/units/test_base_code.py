import unittest
from unittest.mock import patch, MagicMock
from server import app, loadClubs, loadCompetitions, saveClubs, saveCompetitions
from datetime import datetime

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        # Set up mocked test data before each test
        self.initial_clubs = [
            {"name": "Club1", "email": "club1@example.com", "points": 10},
            {"name": "Club2", "email": "club2@example.com", "points": 15},
        ]
        self.initial_competitions = [
            {"name": "Comp1", "date": "2022-03-01 12:00:00", "numberOfPlaces": 20},
            {"name": "Comp2", "date": "2022-04-01 14:00:00", "numberOfPlaces": 15},
        ]

        # Mock the functions that interact with the data
        with patch('server.loadClubs', return_value=self.initial_clubs):
            with patch('server.loadCompetitions', return_value=self.initial_competitions):
                with patch('server.saveClubs') as mock_save_clubs, \
                        patch('server.saveCompetitions') as mock_save_competitions:
                    # Provide a MagicMock for the mocked save functions
                    mock_save_clubs.side_effect = MagicMock()
                    mock_save_competitions.side_effect = MagicMock()

                    # Continue with the test setup
                    app.config['TESTING'] = True
                    self.app = app.test_client()

    def tearDown(self):
        # Reset data after each test
        self.initial_clubs = []
        self.initial_competitions = []

    def test_index_route(self):
        with self.app as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_show_summary_route_valid_email(self):
        
        with app.test_client() as client:
            response = client.post('/showSummary', data={'email': 'club1@example.com'})
            self.assertEqual(response.status_code, 302)


    def test_show_summary_route_invalid_email(self):
        with self.app as client:
            response = client.post('/showSummary', data={'email': 'invalid@example.com'})
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.location.endswith('/'))
            redirected_response = client.get(response.location)
            self.assertIn(b'Invalid email, please try again.', redirected_response.data)

    def test_purchase_places_route_invalid_competition_or_club(self):
        with self.app as client:
            response = client.post('/purchasePlaces', data={'competition': 'InvalidComp', 'club': 'Club1', 'places': '5'})
            self.assertIn(b"Something went wrong-please try again", response.data)

    def test_display_points_route(self):
        with self.app as client:
            response = client.get('/points')
            self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        with self.app as client:
            response = client.get('/logout')
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.location.endswith('/'))

if __name__ == '__main__':
    unittest.main()
