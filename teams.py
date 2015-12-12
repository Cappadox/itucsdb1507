import psycopg2 as dbapi2

class Team:
    def __init__(self, team_id, name, league_id):
        self.team_id = team_id
        self.name = name
        self.league_id = league_id

class Teams:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS TEAMS
                    (
                    TEAM_ID serial NOT NULL PRIMARY KEY,
                    NAME varchar(100) NOT NULL,
                    LEAGUE_ID int NOT NULL REFERENCES LEAGUES(LEAGUE_ID)
                    )
                    """)
                connection.commit()

    def select_teams(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM TEAMS ORDER BY TEAM_ID """
             cursor.execute(query)
             connection.commit()

             teams = cursor.fetchall()
             return teams

    def get_team(self, team_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM TEAMS WHERE TEAM_ID = %s """
             cursor.execute(query, [team_id])
             connection.commit()
             team = cursor.fetchall()
             return team

    def delete_team(self, team_id):
         with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """ DELETE FROM TEAMS WHERE TEAM_ID = %s """
            cursor.execute(query, [team_id])
            connection.commit()

    def add_team(self, name, league_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO TEAMS (NAME, LEAGUE_ID) VALUES (%s, %s) """
                cursor.execute(query, (name, league_id))
                connection.commit()

    def update_team(self, team_id, name, league_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE TEAMS
                        SET NAME = %s,
                        LEAGUE_ID = %s
                        WHERE
                        TEAM_ID = %s """
                cursor.execute(query, (name, league_id, team_id))
                connection.commit()

    def search_team(self, name):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ SELECT * FROM TEAMS WHERE NAME LIKE %s ORDER BY TEAM_ID """
                cursor.execute(query, ['%'+name+'%'])
                teams = cursor.fetchall()
                return teams

    def get_team_name(self, team_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM TEAMS WHERE TEAM_ID = %s"""
             cursor.execute(query, [team_id])
             key,name,league = cursor.fetchone()
             return name

    def select_team_names(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT NAME FROM TEAMS ORDER BY TEAM_ID """
             cursor.execute(query)
             connection.commit()

             names = cursor.fetchall()
             return names

