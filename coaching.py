import psycopg2 as dbapi2

class Coaching:
    def __init__(self, team_id, coach_id,season_id):
        self.team_id = team_id
        self.coach_id = coach_id
        self.season_id = season_id

class Coaching2:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS COACHING
                (
                TEAM_ID INT NOT NULL REFERENCES TEAMS(TEAM_ID),
                COACH_ID INT NOT NULL REFERENCES COACHES(COACH_ID),
                SEASON_ID INT NOT NULL REFERENCES SEASONS(SEASON_ID)
                ) """)
                connection.commit()

    def select_coaching(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM COACHING"""
             cursor.execute(query)
             result = cursor.fetchall()
             return result

    def add_coaching(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()

                connection.commit()

    def delete_coaching(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:

                connection.commit()