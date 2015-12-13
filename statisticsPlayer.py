import psycopg2 as dbapi2

class StatisticP:
    def __init__(self, statistic_id, season, playerName, tackles, penalties):
        self.statistic_id = statistic_id
        self.season = season
        self.playerName = playerName
        self.tackles = tackles
        self.penalties = penalties

class StatisticsP:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS STATISTICSP
                    (
                    STATISTIC_ID SERIAL NOT NULL PRIMARY KEY,
                    SEASON_ID INTEGER NOT NULL REFERENCES SEASONS(SEASON_ID),
                    PLAYER_ID INTEGER NOT NULL REFERENCES PLAYERS(PLAYER_ID),
                    tackles INTEGER NOT NULL,
                    penalties INTEGER NOT NULL
                    )
                    """)
                connection.commit()

    def get_statistics_player(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM STATISTICSP"""
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    def add_statistic_player(self, season_id, player_id, tackles, penalties):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO STATISTICSP (SEASON_ID, PLAYER_ID, tackles, penalties) VALUES (%s, %s, %s, %s) """
                cursor.execute(query, (season_id, player_id, tackles, penalties))
                connection.commit()

    def delete_statistic_player(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM STATISTICSP
                    WHERE STATISTIC_ID = %s""",
                    id)
                connection.commit()

    def update_statistic_player(self, statistic_id, season_id, player_id, tackles, penalties):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE STATISTICSP
                        SET SEASON_ID = %s,
                        PLAYER_ID = %s,
                        TACKLES = %s,
                        PENALTIES = %s
                        WHERE STATISTIC_ID = %s"""
                cursor.execute(query, (season_id, player_id, tackles, penalties, statistic_id))
                connection.commit()

    def search_statistic_player(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM STATISTICSP
                    WHERE CAST(PLAYER_ID as VARCHAR(30)) LIKE '%s'
                    ORDER BY STATISTIC_ID ASC""" % (('%'+id+'%'))
            cursor.execute(query)
            connection.commit()

            result = cursor.fetchall()
            return result
