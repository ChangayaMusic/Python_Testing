import json
from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 5)  # simulated user wait time between tasks

    def on_start(self):
        self.user_index = 0
        # Load clubs and competitions from JSON files
        with open("clubs.json") as f:
            self.clubs = json.load(f)["clubs"]
        with open("competitions.json") as f:
            self.competitions = json.load(f)["competitions"]

    @task
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        # Pick a random club email for testing
        email = self.clubs[self.user_index % len(self.clubs)]["email"]
        self.client.post("/showSummary", data={"email": email})

    @task
    def book_competition(self):
        # Pick a random competition and club for testing
        competition = self.competitions[self.user_index % len(self.competitions)]["name"]
        club = self.clubs[self.user_index % len(self.clubs)]["name"]
        self.client.get(f"/book/{competition}/{club}")

    @task
    def purchase_places(self):
        # Pick a random competition and club for testing
        competition = self.competitions[self.user_index % len(self.competitions)]["name"]
        club = self.clubs[self.user_index % len(self.clubs)]["name"]
        places = 3  # Number of places to purchase
        data = {
            "competition": competition,
            "club": club,
            "places": places
        }
        self.client.post("/purchasePlaces", data=data)

    @task
    def display_points(self):
        self.client.get("/points")

    @task
    def logout(self):
        self.client.get("/logout")