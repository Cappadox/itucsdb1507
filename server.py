import datetime
import json
import os
import psycopg2 as dbapi2
import re

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask.helpers import url_for
from team import Team
from user import User
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from warnings import catch_warnings


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
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/teams')
def teams():
    now = datetime.datetime.now()
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ SELECT * FROM TEAMS"""
        cursor.execute(query)
        result = cursor.fetchall()
    return render_template('teams.html', current_time=now.ctime(), result = result)

@app.route('/players')
@login_required
def players():
    now = datetime.datetime.now()
    return render_template('players.html', current_time=now.ctime())

@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/initdb')
def create_tables():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS TEAMS
        (
        ID INTEGER PRIMARY KEY,
        NAME VARCHAR(50) NOT NULL,
        YEAR INTEGER NOT NULL,
        STANDING INTEGER,
        AVGFAN FLOAT
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS PLAYERS
        (
        ID INTEGER PRIMARY KEY,
        NAME VARCHAR(50) NOT NULL,
        TEAMID INTEGER REFERENCES TEAMS(ID),
        AGE INTEGER NOT NULL,
        KITNO INTEGER
        ) """

        cursor.execute(query)
        query = """CREATE TABLE IF NOT EXISTS USERS
        (
        ID SERIAL PRIMARY KEY,
        USER_NAME VARCHAR(50) NOT NULL UNIQUE,
        USER_PASSWORD VARCHAR(50) NOT NULL,
        USER_TYPE VARCHAR(30) NOT NULL
        )"""
        cursor.execute(query)

        query = """INSERT INTO USERS
        (ID, USER_NAME, USER_PASSWORD)
        VALUES (1, 'alparslan', 'alpi94')"""
        cursor.execute(query)
        connection.commit()

    return redirect(url_for('home_page'))

@app.route('/addteam', methods = ['GET', 'POST'])
def add_team():
        id = request.form.get("id")
        name = request.form.get("name")
        year = request.form.get("year")
        standing = request.form.get("standing")
        avgfan = request.form.get("avgfan")

        team = Team(id,name,year,standing,avgfan)

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """ INSERT INTO TEAMS (ID, NAME, YEAR, STANDING, AVGFAN) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (id, name, year, standing, avgfan))
            connection.commit()

        return redirect(url_for('teams'))



if __name__ == '__main__':
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