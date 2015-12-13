import psycopg2 as dbapi2

class Coaches:
    def __init__(self, id, name,birthday):
        self.id = id
        self.name = name
        self.birthday = birthday

class Coaches2:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS COACHES
                (
                COACH_ID SERIAL PRIMARY KEY,
                NAME VARCHAR(50) NOT NULL,
                BIRTHDAY INTEGER NOT NULL
                ) """)
                connection.commit()

    def select_coaches(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM COACHES ORDER BY COACH_ID ASC"""
             cursor.execute(query)
             result = cursor.fetchall()
             return result

    def add_coach(self, name, birthday):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO COACHES (NAME, BIRTHDAY) VALUES (%s, %s) """
                cursor.execute(query, (name, birthday))
                connection.commit()
    def search_coach(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """  """
                cursor.execute(query, [id])
                connection.commit()

    def delete_coach(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ DELETE FROM COACHES WHERE COACH_ID =%s """
                cursor.execute(query, [id])
                connection.commit()

    def update_coach(self, coach_id, name, birthday):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE COACHES SET NAME = %s, BIRTHDAY= %s WHERE COACH_ID = %s """
                cursor.execute(query, (name,birthday,coach_id))
                connection.commit()