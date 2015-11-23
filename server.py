import psycopg2 as dbapi2
import datetime
import json
import os
import re

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask.helpers import url_for

from coaches import Coaches, Coaches2
from coaching import Coaching,Coaching2
from countries import Countries, Country
from leagues import Leagues, League
from matches import Matches, Match
from teams import Team, Teams
from officials import Officials, Official
from players import Player, Players
from seasons import Seasons, Seasons2
from statistics import Statistic, Statistics
from fixtures import Fixture, Fixtures
from flask.templating import render_template_string


app = Flask(__name__)

'''ElephantSQL configurations'''
def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

'''Home Page'''
@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


'''Coaches Pages'''
@app.route('/coaches', methods=['GET', 'POST'])
def coaches():
    if request.method == 'GET':
        return render_template('coaches.html', result = app.coaches.select_coaches())
    else:
        if 'Add' in request.form:
            name = request.form['coachName']
            birthday = request.form['coachBirthday']
            app.coaches.add_coach(name, birthday)
            return redirect(url_for('coaches'))
        elif 'Delete' in request.form:
            id = request.form['id']
            app.coaches.delete_coach(id)
            return redirect(url_for('coaches'))
        else:
            return render_template('coaches.html', result = app.coaches.select_coaches())

'''Coaching Pages'''
@app.route('/coaching', methods=['GET', 'POST'])
def coaching():
    if request.method == 'GET':
        return render_template('coaching.html', result = app.coaching.select_coaching())
    else:
        if 'Add' in request.form:

            return redirect(url_for('coaching'))
        elif 'Delete' in request.form:

            return redirect(url_for('coaching'))
        else:
            return render_template('coaching.html', result = app.coaching.select_coaching())


'''Countries Pages'''
@app.route('/countries', methods=['GET', 'POST'])
def countries():
    if request.method == 'GET':
        return render_template('countries.html', countries = app.countries.get_countries())
    else:
        name = request.form['name']
        abbreviation = request.form['abbreviation']
        app.countries.add_country(Country(name, abbreviation))
        return redirect(url_for('countries'))

@app.route('/countries/add')
def countries_edit():
     return render_template('country_edit.html')


'''Fixtures Pages'''
@app.route('/fixtures', methods = ['GET', 'POST'])
def fixtures():
    if request.method == 'GET':
        return render_template('fixtures.html', result = app.fixtures.get_fixtures())
    else:
        season = request.form['season']
        team = request.form['team']
        points = request.form['points']
        app.fixtures.add_fixture(season, team, points)
    return redirect(url_for('fixtures'))


'''Officials Pages'''
@app.route('/officials', methods=['GET', 'POST'])
def officials():
    if request.method == 'GET':
        return render_template('officials.html', officials = app.officials.get_officials())
    else:
        name = request.form['name']
        age = request.form['age']
        app.officials.add_official(name, age)
        return redirect(url_for('officials'))

@app.route('/officials/add', methods=['GET', 'POST'])
def official_add():
     return render_template('official_edit.html')

@app.route('/officials/delete', methods=['GET', 'POST'])
def official_delete():
    if request.method == 'GET':
        return render_template_string("""You need to click delete button at the end of the desired official.
                                            Return to the list of officials.
                                            <form action="{{ url_for('officials') }}" method="get" role="form">
                                            <div class="form-group">
                                            <input value="Return" name="Return" type="submit" /><br><br>
                                            </div> <!-- End of form-group -->
                                            </form>""")
    else:
        id = request.form['id']
        app.officials.delete_official(id)
        return redirect(url_for('officials'))

'''Leagues Pages'''
@app.route('/leagues', methods=['GET', 'POST'])
def leagues():
    if request.method == 'GET':
        return render_template('leagues.html', leagues = app.leagues.get_leagues())
    else:
        name = request.form['name']
        abbreviation =request.form['abbreviation']
        countryID = request.form['countryID']
        app.leagues.add_league(League(name, abbreviation, countryID))
        return redirect(url_for('leagues'))

@app.route('/leagues/add')
def leagues_edit():
    return render_template('league_edit.html', countries = app.countries.get_countries())


'''Player Pages'''
@app.route('/players', methods=['GET', 'POST'])
def players():
    if request.method == 'GET':
        return render_template('players.html', result = app.players.select_players())
    else:
        name = request.form['name']
        birthday = request.form['birthday']
        position = request.form['position']
        app.players.add_player(name, birthday, position)
    return redirect(url_for('players'))

@app.route('/players/add', methods=['GET', 'POST'])
def add_players():
    return render_template('players_add.html')

@app.route('/players/update/<player_id>', methods=['GET', 'POST'])
def update_players(player_id):
    if request.method == 'GET':
        return render_template('players_edit.html', player = app.players.get_player(player_id))
    else:
        name = request.form['name']
        birthday = request.form['birthday']
        position = request.form['position']
        app.players.update_player(player_id, name, birthday, position)
        return redirect(url_for('players'))

@app.route('/players/delete', methods=['GET', 'POST'])
def delete_players():
    if request.method == 'GET':
        return redirect(url_for('teams'))
    elif 'checkbox' in request.form:
        ids = request.form.getlist('checkbox')
        for id in ids:
            app.players.delete_player(id)
        return redirect(url_for('players'))


'''Seasons Pages'''
@app.route('/seasons', methods=['GET', 'POST'])
def seasons():
    if request.method == 'GET':
        return render_template('seasons.html', result = app.seasons.select_seasons())
    else:
        if 'Add' in request.form:
            year = request.form['seasonYear']
            app.seasons.add_season(year)
            return redirect(url_for('seasons'))
        elif 'Delete' in request.form:
            id = request.form['id']
            app.seasons.delete_season(id)
            return redirect(url_for('seasons'))
        else:
            return render_template('seasons.html', result = app.seasons.select_seasons())


'''Statistics Pages'''
@app.route('/statistics', methods = ['GET', 'POST'])
def statistics():
    if request.method == 'GET':
        return render_template('statistics.html', result = app.statistics.get_statistics())
    else:
        season = request.form['season']
        playerName = request.form['playerName']
        receptions = request.form['receptions']
        receivingyards = request.form['receivingyards']
        app.statistics.add_statistic(season, playerName, receptions, receivingyards)
    return redirect(url_for('statistics'))


'''Team pages'''
@app.route('/teams', methods=['GET', 'POST'])
def teams():
    if request.method == 'GET':
        return render_template('teams.html', teams = app.teams.select_teams())
    else:
        name = request.form['name']
        league_id = request.form['league_id']
        app.teams.add_team(name,league_id)
    return redirect(url_for('teams'))

@app.route('/teams/add', methods=['GET', 'POST'])
def add_teams():
    return render_template('teams_add.html')

@app.route('/teams/update/<team_id>', methods=['GET', 'POST'])
def update_teams(team_id):
    if request.method == 'GET':
        return render_template('teams_edit.html', team = app.teams.get_team(team_id))
    else:
        name = request.form['name']
        league_id = request.form['league_id']
        app.teams.update_team(team_id, name, league_id)
        return redirect(url_for('teams'))

@app.route('/teams/delete', methods=['GET', 'POST'])
def delete_teams():
    if request.method == 'GET':
        return redirect(url_for('teams'))
    elif 'checkbox' in request.form:
        ids = request.form.getlist('checkbox')
        for id in ids:
            app.teams.delete_team(id)
        return redirect(url_for('teams'))


'''Database initialization'''
@app.route('/initdb')
def create_tables():

    '''Reference order in DB should be preserved'''
    app.coaches.initialize_tables()
    app.seasons.initialize_tables()
    app.countries.initialize_tables()
    app.players.initialize_tables()
    app.leagues.initialize_tables()
    app.teams.initialize_tables()
    app.coaching.initialize_tables()

    app.officials.initialize_tables()
    app.matches.initialize_tables()

    app.statistics.initialize_tables()
    app.fixtures.initialize_tables()

    return redirect(url_for('home_page'))


if __name__ == '__main__':

    '''Container objects'''

    app.coaches = Coaches2(app)
    app.coaching = Coaching2(app)
    app.teams = Teams(app)
    app.players = Players(app)
    app.countries = Countries(app)
    app.leagues = Leagues(app)
    app.officials = Officials(app)
    app.matches = Matches(app)
    app.seasons = Seasons2(app)
    app.statistics = Statistics(app)
    app.fixtures = Fixtures(app)

    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
          app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=54321 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)