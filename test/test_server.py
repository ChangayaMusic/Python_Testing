from server import loadClubs, loadCompetitions, app


def test_loadClubs(validate_club):
    """
    a test will check if validate club json variable is in the json initial file
    @param validate_club: a json variable which is included in the json initial file
    """
    file_loadclubs = loadClubs()

    assert validate_club in file_loadclubs



def test_loadCompetitions(validate_competition):
    """
    a test will check if validate competition json variable is in the json initial file
    @param validate_competition:  a json variable which is included in the json initial file
    """
    file = loadCompetitions()
    assert validate_competition in file

        
def test_index(client):
    """
    a test will check if client request root page return a status code 200(successfully connected) and welcome page
    display
    @param client: a fixture provide a test client for the flask
    """
    response = client.get('/')

    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data


class TestshowSummary:

    def test_showSummary_with_validate_email(self, client, validate_club):
        """
        a test will check if client request showsummary page with validate email provide in initial json file return a
        status code 200(successfully connected) and html page display
        @param client: a fixture provide a test client for the flask,
               validate_club: a json variable which is included in the json initial file
               validate_competition:  a json variable which is included in the json initial file
        """
        validate_club_email = validate_club['email']
        response = client.post('/showSummary', data={'email': validate_club_email})

        assert b'Welcome' in response.data
        assert response.status_code == 200

    def test_showSummary_with_unvalidate_email(self, client):
        """
        a test will check if client request showsummary page with no validate email provide in initial json file return
        a status code 401(Unauthorized connection) and html page display
        @param client: a fixture provide a test client for the flask,
               validate_club: a json variable which is included in the json initial file
               validate_competition:  a json variable which is included in the json initial file
        """
        response = client.post('/showSummary', data={'email': '11@irontemple.com'})

        assert b'The email is not found' in response.data
        assert response.status_code == 401


class Testbook:
    def test_book_valid_competition(self, client, validate_club, validate_competition):
        """
        a test will check if client request book page with validate competition data(competition date is in the
        future) return a status code 200(successfully connected) and html page display
        @param client: a fixture provide a test client for the flask,
               validate_club: a json variable which is included in the json initial file
               validate_competition:  a json variable which is included in the json initial file
        """
        competition = validate_competition['name']
        club = validate_club['name']

        response = client.get(f'/book/{competition}/{club}')

        assert response.status_code == 200

    def test_book_competition_finished(self, client, validate_club, competition_past):
        """
        a test will check if client request book page with no validate competition data(competition date is in the
        past) return a status code 403(forbidden) and html page display
        @param client: a fixture provide a test client for the flask,
               validate_club: a json variable which is included in the json initial file
               validate_competition:  a json variable which is included in the json initial file
        """
        competition = competition_past['name']
        club = validate_club['name']

        response = client.get(f'/book/{competition}/{club}')

        assert response.status_code == 403
        assert b'The competition is finished !' in response.data


class TestpurchasePlaces:
    def test_purchasePlaces_success(self, client, validate_club, validate_competition):
        """
        a test will check if client request purchase page with validate purchase data(places required is less than 12
        and less than the points left of the club) return a status code 200(successfully connected) and welcome page
        display.
        @param client: a fixture provide a test client for the flask,
               validate_club: a json variable which is included in the json initial file
               validate_competition:  a json variable which is included in the json initial file
        """
        competition = validate_competition['name']
        club = validate_club['name']
        places_required = 2

        response = client.post('/purchasePlaces',
                               data={'competition': competition, 'club': club, 'places': places_required})

        assert response.status_code == 200

    def test_purchsePlaces_more_than_12_places(self, client, validate_club, validate_competition):
        """
        a test will check if client request purchase page with validate purchase data(places required is more than 12)
        return a status code 403(forbidden) and welcome page
        display.
        @param client: a fixture provide a test client for the flask,
               validate_club: a json variable which is included in the json initial file
               validate_competition:  a json variable which is included in the json initial file
        """
        competition = validate_competition['name']
        club = validate_club['name']
        places_required = 13

        response = client.post('/purchasePlaces',
                               data={'competition': competition, 'club': club, 'places': places_required})

        assert response.status_code == 403
        assert b'You can not reserve more than 12 places' in response.data

    def test_purchsePlaces_more_than_places_availables(self, client, validate_clubs_points_less_than_12,
                                                       validate_competition):
        """
        a test will check if client request purchase page with validate purchase data(places required is more than the
        points left)return a status code 403(forbidden) and welcome page display.
        @param client: a fixture provide a test client for the flask,
               validate_club: a json variable which is included in the json initial file
               validate_competition:  a json variable which is included in the json initial file
        """
        competition = validate_competition
        club = validate_clubs_points_less_than_12
        places_required = int(club['points']) + 1

        response = client.post('/purchasePlaces',
                               data={'competition': competition['name'], 'club': club['name'],
                                     'places': places_required})

        assert response.status_code == 403
        assert b'You do not have enough points to reserve the places' in response.data


def test_show_club_points(client):
    """
    a test will check if client request showclubsandtheirpoints page return a status code 200(successfully connected)
    and right html page display
    @param client: a fixture provide a test client for the flask
    """
    response = client.get('/show_club_points')

    assert response.status_code == 200
    assert b'Lists of clubs and their points || GUDLFT' in response.data


def logout(client):
    """
    a test will check if client request logout page return a status code 200(successfully connected)
    @param client: a fixture provide a test client for the flask
    """
    response = client.get('/logout')

    assert response.status_code == 200