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

from officials import Officials, Official
from countries import Countries, Country
from matches import Matches, Match
from teams import Team, Teams
from players import Player, Players


app = Flask(__name__)


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/teams', methods=['GET', 'POST'])
def teams():
    if request.method == 'GET':
        return render_template('teams.html', result = app.teams.select_teams())
    else:
        name = request.form['name']
        league_id = request.form['league_id']
        app.teams.add_team(name,league_id)
    return redirect(url_for('teams'))

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


@app.route('/coaches')
def coaches():
    now = datetime.datetime.now()
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ SELECT * FROM COACHES"""
        cursor.execute(query)
        result = cursor.fetchall()
    return render_template('coaches.html', current_time=now.ctime(), result = result)

@app.route('/countries', methods=['GET', 'POST'])
def countries_page():
    if request.method == 'GET':
        return render_template('countries.html', countries = app.countries.get_countries())
    else:
        name = request.form['name']
        abbreviation = request.form['abbreviation']
        app.countries.add_country(name, abbreviation)
        return redirect(url_for('countries_page'))

@app.route('/countries/add')
def country_edit_page():
     return render_template('country_edit.html')

@app.route('/initdb')
def create_tables():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS COACHES
        (
        COACH_ID SERIAL PRIMARY KEY,
        NAME VARCHAR(50) NOT NULL,
        BIRTHDAY INTEGER NOT NULL
        ) """
        cursor.execute(query)

        connection.commit()

        app.teams.initialize_tables()
        app.players.initialize_tables()
        app.countries.initialize_tables()
        app.officials.initialize_tables()
        app.matches.initialize_tables()

    return redirect(url_for('home_page'))

@app.route('/addcoach', methods = ['GET', 'POST'])
def add_coach():
        name = request.form.get("coachName")
        birthday = request.form.get("coachBirthday")


        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """ INSERT INTO COACHES (NAME, BIRTHDAY) VALUES (%s, %s)"""
            cursor.execute(query, (name, birthday))
            connection.commit()

        return redirect(url_for('coaches'))

if __name__ == '__main__':
    app.teams = Teams(app)
    app.players = Players(app)
    app.countries = Countries(app)
    app.officials = Officials(app)
    app.matches = Matches(app)
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