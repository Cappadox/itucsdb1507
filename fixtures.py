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
            query="""SELECT F.FIXTURE_ID, S.YEAR, T.NAME, F.POINTS
                        FROM FIXTURES F
                        LEFT JOIN SEASONS S ON (F.SEASON_ID = S.SEASON_ID)
                        LEFT JOIN TEAMS T ON (F.TEAM_ID = T.TEAM_ID)
                        ORDER BY S.YEAR ASC"""
            cursor.execute(query)
            connection.commit()

            fixtures = [(key, season, team, points)
                        for key, season, team, points in cursor]
            return fixtures

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

    def update_fixture(self, fixture_id, season_id, team_id, points):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE FIXTURES
                        SET SEASON_ID = %s,
                        TEAM_ID = %s,
                        POINTS = %s
                        WHERE FIXTURE_ID = %s"""
                cursor.execute(query, (season_id, team_id, points, fixture_id))
                connection.commit()

    def search_fixture(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT FIXTURE_ID, SEASONS.YEAR, TEAMS.NAME, POINTS
                    FROM FIXTURES
                    INNER JOIN SEASONS ON SEASONS.SEASON_ID=FIXTURES.SEASON_ID
                    INNER JOIN TEAMS ON TEAMS.TEAM_ID=FIXTURES.TEAM_ID
                    WHERE TEAMS.NAME LIKE '%s'""" % ('%'+id+'%')
            cursor.execute(query)
            connection.commit()

            result = cursor.fetchall()
            return result