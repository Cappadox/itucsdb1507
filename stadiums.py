import psycopg2 as dbapi2

class Stadium:
    def __init__(self, name, capacity, country_id, team_id):
        self.name = name
        self.capacity = capacity
        self.country_id = country_id
        self.team_id = team_id

class Stadiums:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS STADIUMS (
                        STADIUM_ID serial  NOT NULL,
                        NAME varchar(100)  NOT NULL,
                        CAPACITY int  NULL,
                        COUNTRY_ID int  NOT NULL,
                        TEAM_ID int  NOT NULL,
                        CONSTRAINT STADIUMS_pk
                            PRIMARY KEY (STADIUM_ID),
                        CONSTRAINT STADIUMS_COUNTRIES
                            FOREIGN KEY (COUNTRY_ID)
                            REFERENCES COUNTRIES (COUNTRY_ID)
                            ON DELETE RESTRICT,
                        CONSTRAINT STADIUMS_TEAMS
                            FOREIGN KEY (TEAM_ID)
                            REFERENCES TEAMS (TEAM_ID)
                            ON DELETE RESTRICT
                    );
                    """)
        connection.commit()


    def add_stadium(self, name, capacity, country_id, team_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query ="""
                    INSERT INTO STADIUMS (NAME, CAPACITY, COUNTRY_ID, TEAM_ID)
                        VALUES (%s, %s, %s, %s) """
                cursor.execute(query, (name, capacity, country_id, team_id))
                connection.commit()

    def delete_stadium(self, stadium_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ DELETE FROM STADIUMS WHERE STADIUM_ID =%s """
                cursor.execute(query, [stadium_id])
                connection.commit()

    def get_stadium(self, stadium_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM STADIUMS
                        WHERE STADIUM_ID =%s """
            cursor.execute(query, (stadium_id))
            connection.commit()

            stadium_id, name, capacity, country_id, team_id = cursor.fetchone()
            return stadium_id, name, capacity, country_id, team_id

    def get_stadiums(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT S.STADIUM_ID, S.NAME, S.CAPACITY, C.NAME, T.NAME
                        FROM  STADIUMS S
                        LEFT JOIN COUNTRIES C ON (S.COUNTRY_ID = C.COUNTRY_ID)
                        LEFT JOIN TEAMS T ON (S.TEAM_ID = T.TEAM_ID)
                        """
            cursor.execute(query)
            connection.commit()

            stadiums = [(key, name, capacity, country, team)
                        for key, name, capacity, country, team in cursor]

            return stadiums

    def update_stadium(self, stadium_id, name, capacity, country_id, team_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE STADIUMS
                                SET NAME = %s, CAPACITY = %s, COUNTRY_ID = %s, TEAM_ID = %s
                            WHERE STADIUM_ID = %s """
                cursor.execute(query, (name, capacity, country_id, team_id, stadium_id))
                connection.commit()

    def search_stadiums(self, search_terms):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT S.STADIUM_ID, S.NAME, S.CAPACITY, C.NAME, T.NAME
                        FROM  STADIUMS S
                        LEFT JOIN COUNTRIES C ON (S.COUNTRY_ID = C.COUNTRY_ID)
                        LEFT JOIN TEAMS T ON (S.TEAM_ID = T.TEAM_ID)
                        WHERE S.NAME LIKE '%s' ORDER BY S.NAME""" % (('%'+search_terms+'%'))
            cursor.execute(query)
            connection.commit()
            stadiums = [(key, name, capacity, country, team)
                        for key, name, capacity, country, team in cursor]

            return stadiums



