import psycopg2 as dbapi2
from teams import Team,Teams
from players import Player,Players
from seasons import Seasons,Seasons2

class Transfer:
    def __init__(self, season_id, player_id, old_id, new_id, fee,
                season="123", player_name="Default Player", old_team="Default Old",
                new_team="Default New"):
        self.season_id=season_id
        self.player_id=player_id
        self.old_id=old_id
        self.new_id=new_id
        self.fee=fee
        self.season=season
        self.player_name=player_name
        self.old_team=old_team
        self.new_team=new_team

class Transfers:
    def __init__(self, app):
        self.app = app
        self.app.teams = Teams(app)
        self.app.players = Players(app)
        self.app.seasons = Seasons2(app)

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS TRANSFERS (
                        TRANSFER_ID SERIAL NOT NULL PRIMARY KEY,
                        SEASON_ID int NOT NULL REFERENCES SEASONS(SEASON_ID),
                        OLD_ID int NOT NULL REFERENCES TEAMS(TEAM_ID),
                        NEW_ID int NOT NULL REFERENCES TEAMS(TEAM_ID),
                        PLAYER_ID int REFERENCES PLAYERS(PLAYER_ID),
                        FEE VARCHAR(30) NOT NULL
                        );""")

                connection.commit()

    def add_transfer(self, transfer):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO TRANSFERS (SEASON_ID, OLD_ID, NEW_ID, PLAYER_ID, FEE)
                    VALUES (%s, %s, %s, %s, %s) """,
                    (transfer.season_id, transfer.old_id, transfer.new_id, transfer.player_id, transfer.fee))
                connection.commit()

    def delete_transfer(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM TRANSFERS
                    WHERE TRANSFER_ID = %s""",
                    id)
                connection.commit()

    def update_transfer(self, id, transfer):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE TRANSFERS
                        SET SEASON_ID = %s, OLD_ID = %s,
                        NEW_ID = %s, PLAYER_ID = %s,
                        FEE = %s
                        WHERE TRANSFER_ID = %s """
                cursor.execute(query, (transfer.season_id, transfer.old_id,
                                       transfer.new_id, transfer.player_id,
                                       transfer.fee, id))
                connection.commit()

    def get_transfers(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT T.TRANSFER_ID, T1.NAME, T2.NAME, S.YEAR, P.NAME, T.FEE
                    FROM TRANSFERS T
                    JOIN TEAMS T1 ON T1.TEAM_ID=T.OLD_ID
                    JOIN TEAMS T2 ON T2.TEAM_ID=T.NEW_ID
                    JOIN SEASONS S ON S.SEASON_ID=T.SEASON_ID
                    JOIN PLAYERS P ON P.PLAYER_ID=T.PLAYER_ID"""
            cursor.execute(query)
            connection.commit()

            transfers = [(key, Transfer("1", "1", "1", "1", fee, season,
                                       player_name, old_team, new_team))
                        for key, old_team, new_team, season, player_name, fee in cursor]

            return transfers
