from unittest import TestCase
from server import app, loadClubs, loadCompetitions, saveClubs, saveCompetitions

class GulfTestCase(TestCase):

    def setUp(self):
        # Load initial data before each test
        self.initial_clubs = loadClubs()
        self.initial_competitions = loadCompetitions()

    def tearDown(self):
        # Reset data after each test
        saveClubs(self.initial_clubs)
        saveCompetitions(self.initial_competitions)

    