import psycopg2 as dbapi2

class Official:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Officials:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS OFFICIALS (
                        OFFICIAL_ID SERIAL  NOT NULL PRIMARY KEY,
                        NAME varchar(100)  NOT NULL,
                        AGE INT NOT NULL
                    );""")

                connection.commit()

    def add_official(self, name, age):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO OFFICIALS (NAME, AGE)
                    VALUES (%s, %s) """,
                    (name, age))
                connection.commit()

    def delete_official(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM OFFICIALS
                    WHERE OFFICIAL_ID = %s""",
                    id)
                connection.commit()

    def update_official(self, id, official):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE OFFICIALS
                        SET NAME = %s, AGE = %s
                        WHERE OFFICIAL_ID = %s """
                cursor.execute(query, (official.name, official.age, id))
                connection.commit()

    def get_official(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query="""SELECT * FROM OFFICIALS WHERE OFFICIAL_ID = %s"""
                cursor.execute(query, [id])
                key,name,age = cursor.fetchone();
                return name

    def get_officials(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM OFFICIALS"""
            cursor.execute(query)
            connection.commit()

            officials = [(key, Official(name, age))
                        for key, name, age in cursor]

            return officials

    def search_officials(self, name):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM OFFICIALS
                    WHERE NAME LIKE '%s'""" % (('%'+name+'%'))
            cursor.execute(query)
            connection.commit()
            print(name)

            officials = [(key, Official(name, age))
                        for key, name, age in cursor]

            return officials
