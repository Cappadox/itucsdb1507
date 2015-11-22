import psycopg2 as dbapi2

class Player:
    def __init__(self, player_id, name, birthday, position):
        self.player_id = player_id
        self.name = name
        self.birthday = birthday
        self.position = position

class Players:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS PLAYERS
                    ( PLAYER_ID serial NOT NULL PRIMARY KEY,
                      NAME varchar(100) NOT NULL,
                      BIRTHDAY date NULL,
                      POSITION varchar(100) NULL
                    )
                    """)
                connection.commit()

    def select_players(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM PLAYERS"""
             cursor.execute(query)
             result = cursor.fetchall()
             return result

    def add_player(self, name, birthday, position):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO PLAYERS (NAME, BIRTHDAY, POSITION) VALUES (%s, %s, %s) """
                cursor.execute(query, (name, birthday, position))
                connection.commit()

