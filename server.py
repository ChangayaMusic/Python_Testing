import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime



def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def saveClubs(clubs):
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c, indent=2)


def saveCompetitions(competitions):
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps, indent=2)


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    
    # Use next() with a default value of None
    club = next((club for club in clubs if club['email'] == email), None)

    if club is not None:
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash('Invalid email, please try again.')
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    if foundClub and foundCompetition:
        competition_date = datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S')

        current_date = datetime.now()

        if competition_date < current_date:
            flash("Error: Competition date is in the past")
            return render_template('welcome.html', club=club, competitions=competitions)

        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)
@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    club_name = request.form['club']
    placesRequired = int(request.form['places'])
    competition = next(
        (c for c in competitions if c['name'] == competition_name), None)
    club = next((c for c in clubs if c['name'] == club_name), None)
    
    if competition and club:
        if 0 < placesRequired <= 12:
        
            if placesRequired <= int(club['points']):
                # Convert to int before subtraction
                competition['numberOfPlaces'] = int(
                    competition['numberOfPlaces']) - placesRequired
                # Convert to int before subtraction
                club['points'] = int(club['points']) - placesRequired

                saveClubs(clubs)
                saveCompetitions(competitions)

                flash('Great-booking complete!')
            else:
        
                flash(f"Not enough points in this club to book ")
        else:
            flash("Error: Can't book more than 12 places")    
    else:
        flash("Something went wrong-please try again")


    
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/points')
def displayPoints():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
