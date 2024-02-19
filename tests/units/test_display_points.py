from requests import session, get, post
from json import loads
from bs4 import BeautifulSoup

def test_page_ok():
    response = get("http://127.0.0.1:5000/points")
    assert response.status_code == 200

def test_page_ok_if_logged():
    user_session = session()
    response = user_session.post("http://127.0.0.1:5000/showSummary", data={"email": "admin@irontemple.com"})
    assert response.status_code == 200
    response = user_session.get("http://127.0.0.1:5000/points")
    assert response.status_code == 200

def test_page_structure():
    response = get("http://127.0.0.1:5000/points")
    
    with open('clubs.json', 'r') as clubs_file:
        data = loads(clubs_file.read())
    
    soup = BeautifulSoup(response.text, 'html.parser')
    # There should be a table in html with points
    table = soup.find('table')
    # Verify there is not an unknown club in the table
    for row in table.find('tbody').find_all('tr'):
        valid_club = None
        columns = row.find_all('td')
        # Check if there is the name in the table
        for column in columns:
            for club in data['clubs']:
                if club['name'] == column.text.strip():
                    valid_club = club
                    break  # Break the loop if the club is found

            # Check if the points are present in the table
            points = column.text.strip()
            assert str(valid_club.get("points", "")) == points, f"Expected points: {valid_club.get('points')}, Actual points: {points}"

        # Ensure that a valid club was found for each column in the row
        assert valid_club is not None, "No valid club found for the row"
