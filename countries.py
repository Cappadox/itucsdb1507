import psycopg2 as dbapi2

class Country:
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation

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

    def add_country(self, country):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO COUNTRIES (NAME, ABBREVIATION)
                    VALUES (%s, %s) """,
                    (country.name,country. abbreviation))
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
