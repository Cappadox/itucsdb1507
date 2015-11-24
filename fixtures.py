import psycopg2 as dbapi2

class Fixture:
    def __init__(self, fixture_id, season, team, points):
        self.fixture_id = fixture_id
        self.season = season
        self.team = team
        self.points = points

class Fixtures:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS FIXTURES
                    (
                    FIXTURE_ID SERIAL NOT NULL PRIMARY KEY,
                    SEASON_ID INTEGER NOT NULL REFERENCES SEASONS(SEASON_ID),
                    TEAM_ID INTEGER NOT NULL REFERENCES TEAMS(TEAM_ID),
                    POINTS INTEGER NOT NULL
                    )
                    """)
                connection.commit()

    def get_fixtures(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM FIXTURES"""
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    def add_fixture(self, season_id, team_id, points):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO FIXTURES (SEASON_ID, TEAM_ID, POINTS) VALUES (%s, %s, %s) """
                cursor.execute(query, (season_id, team_id, points))
                connection.commit()

    def delete_fixture(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM FIXTURES
                    WHERE FIXTURE_ID = %s""",
                    id)
                connection.commit()