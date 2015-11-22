import psycopg2 as dbapi2

class Statistic:
    def __init__(self, season, playerName, receptions, receivingyards):
        self.season = season
        self.playerName = playerName
        self.receptions = receptions
        self.receivingyards = receivingyards

class Statistics:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS STATISTICS
                    (
                    SEASON INTEGER NOT NULL,
                    PLAYERNAME VARCHAR(50) NOT NULL,
                    RECEPTIONS INTEGER NOT NULL,
                    RECEIVINGYARDS INTEGER NOT NULL
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

    def add_statistic(self, season, playerName, receptions, receivingyards):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO STATISTICS (SEASON, PLAYERNAME, RECEPTIONS, RECEIVINGYARDS) VALUES (%s, %s, %s, %s) """
                cursor.execute(query, (season, playerName, receptions, receivingyards))
                connection.commit()