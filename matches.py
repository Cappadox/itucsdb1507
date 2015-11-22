import psycopg2 as dbapi2

class Match:
    def __init__(self, id, official_name, home_team, away_team):
        self.name = name

class Matches:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS MATCHES (
                        MATCH_ID SERIAL NOT NULL PRIMARY KEY,
                        SEASON_ID int NOT NULL,
                        HOME_ID int NOT NULL REFERENCES TEAMS(TEAM_ID),
                        VISITOR_ID int NOT NULL REFERENCES TEAMS(TEAM_ID),
                        OFFICIAL_ID int NOT NULL REFERENCES OFFICIALS(OFFICIAL_ID)
                        );""")

                connection.commit()


    def add_match(self, season, home, visitor, official):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO MATCHES (SEASON_ID, HOME_ID, VISITOR_ID, OFFICIAL_ID)
                    VALUES (%s, %s, %s, %s) """,
                    (season, home, visitor, official))
                connection.commit()


    def get_matches(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM COUNTRIES"""
            cursor.execute(query)
            connection.commit()

            countries = [(key, Country(name, abbreviation))
                        for key, name, abbreviation in cursor]

            return countries
