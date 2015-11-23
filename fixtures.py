import psycopg2 as dbapi2

class Fixture:
    def __init__(self, season, team, points):
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
                    SEASON INTEGER NOT NULL,
                    TEAM VARCHAR(50) NOT NULL,
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

    def add_fixture(self, season, team, points):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO FIXTURES (SEASON, TEAM, POINTS) VALUES (%s, %s, %s) """
                cursor.execute(query, (season, team, points))
                connection.commit()