import psycopg2 as dbapi2

class Team:
    def __init__(self, app):
        self.app = app

    def initialize_table(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE TEAMS
                    (
                    TEAM_ID serial NOT NULL PRIMARY KEY,
                    NAME varchar(100) NOT NULL,
                    LEAGUE_ID int NOT NULL
                    )
                    """)
                connection.commit()

    def select_teams(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM TEAMS"""
             cursor.execute(query)
             result = cursor.fetchall()
             return result

    def add_team(self, name, league_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO TEAMS (NAME, LEAGUE_ID) VALUES (%s, %s) """
                cursor.execute(query, (name, league_id))
                connection.commit()

