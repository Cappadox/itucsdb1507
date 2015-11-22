import psycopg2 as dbapi2

class Official:
    def __init__(self, name):
        self.name = name

class Officials:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS OFFICIALS (
                        OFFICIAL_ID SERIAL  NOT NULL PRIMARY KEY,
                        NAME varchar(100)  NOT NULL
                    );""")

                connection.commit()

    def add_official(self, name):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO OFFICIALS NAME
                    VALUES %s """,
                    (name))
                connection.commit()


    def get_officials(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM OFFICIALS"""
            cursor.execute(query)
            connection.commit()

            officals = [(key, Official(name))
                        for key, name in cursor]

            return officials
