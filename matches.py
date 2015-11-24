import psycopg2 as dbapi2
from teams import Team,Teams
from officials import Official,Officials
from seasons import Seasons,Seasons2

class Match:
    def __init__(self, season_id, official_id, home_id, away_id, result,
                season="123", official_name="Default Off.", home_team="Default Home",
                away_team="Default Away"):
        self.season_id=season_id
        self.official_id=official_id
        self.home_id=home_id
        self.away_id=away_id
        self.season=season
        self.official_name=official_name
        self.home_team=home_team
        self.away_team=away_team
        self.result=result


class Matches:
    def __init__(self, app):
        self.app = app
        self.app.teams = Teams(app)
        self.app.officials = Officials(app)
        self.app.seasons = Seasons2(app)

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS MATCHES (
                        MATCH_ID SERIAL NOT NULL PRIMARY KEY,
                        SEASON_ID int NOT NULL REFERENCES SEASONS(SEASON_ID),
                        HOME_ID int NOT NULL REFERENCES TEAMS(TEAM_ID),
                        VISITOR_ID int NOT NULL REFERENCES TEAMS(TEAM_ID),
                        OFFICIAL_ID int REFERENCES OFFICIALS(OFFICIAL_ID),
                        RESULT VARCHAR(30) NOT NULL
                        );""")

                connection.commit()


    def add_match(self, match):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO MATCHES (SEASON_ID, HOME_ID, VISITOR_ID, OFFICIAL_ID, RESULT)
                    VALUES (%s, %s, %s, %s, %s) """,
                    (match.season_id, match.home_id, match.away_id, match.official_id, match.result))
                connection.commit()

    def delete_match(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM MATCHES
                    WHERE MATCH_ID = %s""",
                    id)
                connection.commit()

    def update_match(self, id, match):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE MATCHES
                        SET SEASON_ID = %s, HOME_ID = %s,
                        VISITOR_ID = %s, OFFICIAL_ID = %s,
                        RESULT = %s
                        WHERE MATCH_ID = %s """
                cursor.execute(query, (match.season_id, match.home_id,
                                       match.away_id, match.official_id,
                                       match.result, id))
                connection.commit()

    def get_matches(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM MATCHES
                    ORDER BY MATCH_ID ASC"""
            cursor.execute(query)
            connection.commit()

            matches = [(key, Match(season_id, official_id, home_id, away_id, result,
                                   season=self.app.seasons.get_season(season_id),
                                   official_name=self.app.officials.get_official(official_id),
                                   home_team=self.app.teams.get_team_name(home_id),
                                   away_team=self.app.teams.get_team_name(away_id)))
                        for key, season_id, home_id, away_id, official_id, result in cursor]

            return matches
