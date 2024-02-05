import unittest

from server import app, loadClubs, loadCompetitions
from tests.generic.base_test import GulfTestCase

class TestUpdatePoints(GulfTestCase):
    def test_purchase_places(self):
        # Simulate a purchase
        club_name = "Simply Lift"
        competition_name = "Spring Festival"
        places_required = 3

        # Get initial points and places
        initial_club = next(
            (c for c in self.initial_clubs if c['name'] == club_name), None)
        initial_competition = next(
            (c for c in self.initial_competitions if c['name'] == competition_name), None)

        initial_club_points = int(initial_club['points'])
        initial_competition_places = int(initial_competition['numberOfPlaces'])

        # Make a purchase
        with app.test_client() as client:
            client.post('/purchasePlaces', data={
                'competition': competition_name,
                'club': club_name,
                'places': str(places_required)
            })

        # Get updated points and places
        updated_clubs = loadClubs()
        updated_competitions = loadCompetitions()

        updated_club = next(
            (c for c in updated_clubs if c['name'] == club_name), None)
        updated_competition = next(
            (c for c in updated_competitions if c['name'] == competition_name), None)

        updated_club_points = int(updated_club['points'])
        updated_competition_places = int(updated_competition['numberOfPlaces'])

        # Assert that points and places are updated correctly
        self.assertEqual(updated_club_points,
                         initial_club_points - places_required)
        self.assertEqual(updated_competition_places,
                         initial_competition_places - places_required)


if __name__ == '__main__':
    unittest.main()
