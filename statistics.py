import psycopg2 as dbapi2

class Statistic:
    def __init__(self, statistic_id, season, playerName, touchdowns, rushingYards):
        self.statistic_id = statistic_id
        self.season = season
        self.playerName = playerName
        self.touchdowns = touchdowns
        self.rushingYards = rushingYards

class Statistics:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS STATISTICS
                    (
                    STATISTIC_ID SERIAL NOT NULL PRIMARY KEY,
                    SEASON_ID INTEGER NOT NULL REFERENCES SEASONS(SEASON_ID),
                    TEAM_ID INTEGER NOT NULL REFERENCES TEAMS(TEAM_ID),
                    touchdowns INTEGER NOT NULL,
                    rushingYards INTEGER NOT NULL
                    )
                    """)
                connection.commit()

    def get_statistics(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM STATISTICS"""
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    def add_statistic(self, season_id, team_id, touchdowns, rushingYards):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO STATISTICS (SEASON_ID, TEAM_ID, touchdowns, rushingYards) VALUES (%s, %s, %s, %s) """
                cursor.execute(query, (season_id, team_id, touchdowns, rushingYards))
                connection.commit()

    def delete_statistic(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM STATISTICS
                    WHERE STATISTIC_ID = %s""",
                    id)
                connection.commit()