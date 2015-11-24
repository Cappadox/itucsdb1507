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
                    VALUES (%s, %s) """, (country.name,country. abbreviation))
                connection.commit()

    def update_country(self, country_id, country):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE COUNTRIES
                                SET NAME = %s, ABBREVIATION = %s
                            WHERE COUNTRY_ID = %s """
                cursor.execute(query, (country.name,country. abbreviation,country_id ))
                connection.commit()

    def delete_country(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ DELETE FROM COUNTRIES WHERE COUNTRY_ID =%s """
                cursor.execute(query, [id])
                connection.commit()

    def get_country(self, id):
         with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ SELECT * FROM COUNTRIES WHERE COUNTRY_ID =%s """
                cursor.execute(query, [id])

                connection.commit()
                result = cursor.fetchone()
                country = Country(result[1], result[2])
                return country

    def get_countries(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM COUNTRIES ORDER BY NAME"""
            cursor.execute(query)
            connection.commit()
            countries = [(key, Country(name, abbreviation))
                        for key, name, abbreviation in cursor]

            return countries
