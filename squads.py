import psycopg2 as dbapi2

class Squad:
    def __init__(self, squad_id, team_id, player_id, kit_no):
        self.squad_id = squad_id
        self.team_id = team_id
        self.player_id = player_id
        self.kit_no = kit_no

class Squads:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS SQUADS
                    (
                    SQUAD_ID serial NOT NULL PRIMARY KEY,
                    TEAM_ID int NOT NULL REFERENCES TEAMS(TEAM_ID),
                    PLAYER_ID int NOT NULL UNIQUE REFERENCES PLAYERS(PLAYER_ID),
                    KIT_NO int NOT NULL
                    )
                    """)
                connection.commit()

    def show_squads(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT squad_id, teams.name, players.name, kit_no FROM SQUADS
                     LEFT JOIN TEAMS
                     ON SQUADS.TEAM_ID = TEAMS.TEAM_ID
                     LEFT JOIN PLAYERS
                     ON SQUADS.PLAYER_ID = PLAYERS.PLAYER_ID
                     ORDER BY SQUADS.TEAM_ID """
             cursor.execute(query)
             connection.commit()

             squads = cursor.fetchall()
             return squads

    def select_squads(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM SQUADS ORDER BY TEAM_ID """
             cursor.execute(query)
             connection.commit()

             squads = cursor.fetchall()
             return squads

    def get_squad(self, squad_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM SQUADS WHERE SQUAD_ID = %s """
             cursor.execute(query, [squad_id])
             connection.commit()
             squad = cursor.fetchall()
             return squad

    def delete_squad(self, squad_id):
         with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """ DELETE FROM SQUADS WHERE SQUAD_ID = %s """
            cursor.execute(query, [squad_id])
            connection.commit()

    def add_squad(self, team_id, player_id, kit_no):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO SQUADS (TEAM_ID, PLAYER_ID, KIT_NO) VALUES (%s, %s, %s) """
                cursor.execute(query, (team_id, player_id, kit_no))
                connection.commit()

    def update_squad(self, squad_id, team_id, player_id, kit_no):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE SQUADS
                        SET
                        TEAM_ID = %s,
                        PLAYER_ID = %s,
                        KIT_NO = %s
                        WHERE
                        SQUAD_ID = %s """
                cursor.execute(query, (team_id, player_id, kit_no, squad_id))
                connection.commit()
