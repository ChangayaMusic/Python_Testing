import pytest

from server import app


@pytest.fixture
def client():
    """
    fixture to configure and provide a test client for flask
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def validate_club():
    """
    fixture to provide a validate data which is in the initial json file
    """
    data = {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    }
    return data


@pytest.fixture
def validate_clubs_points_less_than_12():
    data = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }
    return data


@pytest.fixture
def validate_competition():
    data = {
        "name": "Spring Festival",
        "date": "2024-03-27 10:00:00",
        "numberOfPlaces": '25'  # Keep it as a string
    }
    return data

@pytest.fixture
def competition_past():
    data = {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13"
    }
    return data