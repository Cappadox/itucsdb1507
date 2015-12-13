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
                COACHING_ID SERIAL NOT NULL PRIMARY KEY,
                TEAM_ID INT NOT NULL REFERENCES TEAMS(TEAM_ID),
                COACH_ID INT NOT NULL REFERENCES COACHES(COACH_ID),
                SEASON_ID INT NOT NULL REFERENCES SEASONS(SEASON_ID)
                ) """)
                connection.commit()

    def select_coaching(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """SELECT * FROM COACHING"""
             cursor.execute(query)
             result = cursor.fetchall()
             return result

    def get_coaching(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ select coaching_id, teams.name, coaches.name, seasons.year
                    from coaching
                    inner join teams on teams.team_id=coaching.team_id
                    inner join coaches on coaches.coach_id=coaching.coach_id
                    inner join seasons on seasons.season_id=coaching.season_id"""
             cursor.execute(query)
             result = cursor.fetchall()
             return result

    def add_coaching(self,team_id,coach_id,season_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO COACHING (TEAM_ID, COACH_ID, SEASON_ID) VALUES (%s, %s, %s) """
                cursor.execute(query, (team_id, coach_id, season_id))
                connection.commit()

    def delete_coaching(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor=connection.cursor()
                query ="""
                    DELETE FROM COACHING
                    WHERE COACHING_ID = %s"""
                cursor.execute(query,[id])
                connection.commit()

    def update_coaching(self, coaching_id, team_id, coach_id, season_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE COACHING
                        SET TEAM_ID = %s,
                        COACH_ID = %s,
                        SEASON_ID = %s
                        WHERE COACHING_ID = %s"""
                cursor.execute(query, [team_id, coach_id, season_id, coaching_id])
                connection.commit()

    def search_coaching(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query=""

            cursor.execute(query)
            connection.commit()

            result = cursor.fetchall()
            return result