import psycopg2 as dbapi2

class League:
    def __init__(self, name, country):
        self.name = name
        self.country = country

class Leagues:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS LEAGUES(
                        LEAGUE_ID serial  NOT NULL,
                        NAME varchar(100)  NOT NULL,
                        COUNTRY_ID int  NOT NULL,
                        CONSTRAINT LEAGUES_pk PRIMARY KEY (LEAGUE_ID),
                        CONSTRAINT LEAGUES_COUNTRIES
                            FOREIGN KEY (COUNTRY_ID)
                            REFERENCES COUNTRIES (COUNTRY_ID)
                    );
                    """)

                connection.commit()

    def add_League(self, name, abbreviation):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO COUNTRIES (NAME, COUNTRY_ID)
                    VALUES (%s, %s) """,
                    (name, country_id))
                connection.commit()


    def get_LEAGUES(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM LEAGUES"""
            cursor.execute(query)
            connection.commit()

            countries = [(key, League(name, country_name))
                        for key, name, abbreviation in cursor]

            return countries
