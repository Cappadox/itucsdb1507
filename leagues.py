import psycopg2 as dbapi2

class League:
    def __init__(self, name,abbreviation, countryID):
        self.name = name
        self.abbreviation = abbreviation
        self.countryID = countryID

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
                        ABBREVIATION varchar(10),
                        COUNTRY_ID int  NOT NULL,
                        CONSTRAINT LEAGUES_pk PRIMARY KEY (LEAGUE_ID),
                        CONSTRAINT LEAGUES_COUNTRIES
                            FOREIGN KEY (COUNTRY_ID)
                            REFERENCES COUNTRIES (COUNTRY_ID)
                            ON DELETE RESTRICT
                    );
                    """)

                connection.commit()

    def add_league(self, league):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO LEAGUES (NAME, ABBREVIATION, COUNTRY_ID)
                    VALUES (%s, %s, %s) """,
                    (league.name, league.abbreviation, league.countryID))
                connection.commit()

    def delete_league(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ DELETE FROM LEAGUES WHERE LEAGUE_ID =%s """
                cursor.execute(query, [id])
                connection.commit()

    def get_league(self, league_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM LEAGUES
                        WHERE LEAGUE_ID =%s """
            cursor.execute(query, [league_id])
            connection.commit()

            league_id, name, abbreviation, country_id = cursor.fetchone()
            return league_id, name, abbreviation, country_id

    def get_leagues(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT L.LEAGUE_ID, L.NAME, L.ABBREVIATION, C.NAME
                        FROM LEAGUES L
                        LEFT JOIN COUNTRIES C ON (L.COUNTRY_ID = C.COUNTRY_ID)
                        """

            cursor.execute(query)
            connection.commit()

            leagues = [(league_id, name, abbreviation, country_name)
                        for league_id, name, abbreviation, country_name in cursor]

            return leagues
    def update_league(self, league_id, name, abbreviation, country_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE LEAGUES
                                SET NAME = %s, ABBREVIATION = %s, COUNTRY_ID = %s
                            WHERE LEAGUE_ID = %s """
                cursor.execute(query, (name, abbreviation, country_id, league_id))
                connection.commit()

    def search_leagues(self, search_terms):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT L.LEAGUE_ID, L.NAME, L.ABBREVIATION, C.NAME
                        FROM LEAGUES L
                        LEFT JOIN COUNTRIES C ON (L.COUNTRY_ID = C.COUNTRY_ID)
                        WHERE L.NAME LIKE '%s' ORDER BY L.NAME""" % (('%'+search_terms+'%'))

            cursor.execute(query)
            connection.commit()

            leagues = [(league_id, name, abbreviation, country_name)
                        for league_id, name, abbreviation, country_name in cursor]

            return leagues


