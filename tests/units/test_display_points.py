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
        data = clubs_file.read()
    
    clubs_data = loads(data)
    soup = BeautifulSoup(response.text, 'html.parser')
    # There should be a table in html with points
    table = soup.find('table')
    # Verify there is not unknown club in table
    for row in table.find('tbody').find_all('tr'):
        valid_club = None
        columns = row.find_all('td')
        # Check if there is the name in table
        for column in columns:
            for club in clubs_data['clubs']:
                if club['name'] == column.text.strip():
                    valid_club = club

        points = 0
        try:
            points = int(column.text.strip())
        except:
            pass
        else:
            # Verify if points amount in html is the same as in json
            assert int(valid_club["points"]) == points

        # if name not in table, test is failed
        assert valid_club