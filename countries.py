import psycopg2 as dbapi2
from country import Country

class Countries:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS COUNTRIES (
                        COUNTRY_ID serial  NOT NULL,
                        NAME varchar(100)  NOT NULL,
                        ABBREVIATION varchar(4)  NULL,
                        CONSTRAINT COUNTRIES_pk PRIMARY KEY (COUNTRY_ID)
                    );""")

                connection.commit()

    def add_country(self, name, abbreviation):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO COUNTRIES (NAME, ABBREVIATION)
                    VALUES (%s, %s) """,
                    (name, abbreviation))
                connection.commit()


    def get_countries(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM COUNTRIES"""
            cursor.execute(query)
            connection.commit()

            countries = [(key, Country(name, abbreviation))
                        for key, name, abbreviation in cursor]

            return countries
