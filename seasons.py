import psycopg2 as dbapi2

class Seasons:
    def __init__(self, id, name,birthday):
        self.id = id
        self.year = year

class Seasons2:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS SEASONS
                (
                SEASON_ID SERIAL PRIMARY KEY,
                YEAR INTEGER NOT NULL
                ) """)
                connection.commit()

    def get_season(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM SEASONS
                         WHERE SEASON_ID = %s"""
             cursor.execute(query,[id])
             season_id,year = cursor.fetchone()
             return year

    def select_seasons(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM SEASONS ORDER BY SEASON_ID ASC"""
             cursor.execute(query)
             result = cursor.fetchall()
             return result

    def add_season(self, year):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO SEASONS (year) VALUES (%s) """
                cursor.execute(query, [year])
                connection.commit()

    def delete_season(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ DELETE FROM SEASONS WHERE SEASON_ID =%s """
                cursor.execute(query, [id])
                connection.commit()

    def search_season(self, year):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM SEASONS
                         WHERE YEAR = %s"""
             cursor.execute(query,[year])
             result = cursor.fetchall(year)
             return result

    def update_season(self, season_id, year):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE SEASONS SET YEAR = %s WHERE SEASON_ID = %s """
                cursor.execute(query, (year,season_id))
                connection.commit()