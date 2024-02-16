from locust import HttpUser, task, between

class MyUser(HttpUser):

    @task
    def purchase_places(self):
        # Using the first competition and club from your JSON data
        competition_name = "Fall Classic"
        club_name = "Simply Lift"

        response = self.client.post("/purchasePlaces", data={
            "competition": competition_name,
            "club": club_name,
            "places": 1  # Adjust the number of places as needed
        })

        if response.status_code == 200:
            # Check if the booking was successful based on content or flash messages
            if "Great-booking complete!" in response.text:
                self.environment.events.request_success.fire(
                    request_type="Purchase Places",
                    name="/purchasePlaces",
                    response_time=response.elapsed.total_seconds(),
                    response_length=len(response.content),
                )
            else:
                self.environment.events.request_failure.fire(
                    request_type="Purchase Places",
                    name="/purchasePlaces",
                    response_time=response.elapsed.total_seconds(),
                    exception="Booking failed",
                )

    @task
    def index_route(self):
        self.client.get('/')

    @task
    def show_summary_route_valid_email(self):
        response = self.client.post('/showSummary', data={'email': 'club1@example.com'})
        

    @task
    def show_summary_route_invalid_email(self):
        response = self.client.post('/showSummary', data={'email': 'invalid@example.com'})
        

    @task
    def purchase_places_route_invalid_competition_or_club(self):
        response = self.client.post('/purchasePlaces', data={'competition': 'InvalidComp', 'club': 'Club1', 'places': '5'})
        

    @task
    def display_points_route(self):
        self.client.get('/points')

    @task
    def logout_route(self):
        self.client.get('/logout')