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
             players = cursor.fetchall()
             return players

    def get_player(self, player_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM PLAYERS WHERE PLAYER_ID = %s"""
             cursor.execute(query, player_id)
             player = cursor.fetchall()
             return player

    def add_player(self, name, birthday, position):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO PLAYERS (NAME, BIRTHDAY, POSITION) VALUES (%s, %s, %s) """
                cursor.execute(query, (name, birthday, position))
                connection.commit()

    def update_player(self, player_id, name, birthday, position):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE PLAYERS
                        SET NAME = %s,
                        BIRTHDAY = %s,
                        POSITION = %s
                        WHERE
                        PLAYER_ID = %s """
                cursor.execute(query, (name, birthday, position, player_id))
                connection.commit()

    def delete_player(self, player_id):
         with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ DELETE FROM PLAYERS
                        WHERE PLAYER_ID = %s """
                cursor.execute(query, (player_id))
                connection.commit()

    def search_player(self, name):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ SELECT * FROM PLAYERS WHERE NAME = %s """
                cursor.execute(query, (name))

                players = cursor.fetchall()
                return players
