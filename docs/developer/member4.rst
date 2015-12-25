Parts Implemented by Seda Yıldırım
==================================

The following three tables were implemented: **Fixtures**, **Player Statistics**, and **Team Statistics**. The tabs Fixtures and Statistics can be seen on the navigation bar above the site interface.
The classes for the respective tables were created with the same method in mind. All classes include the methods below.

* *Initialize Table*: Run a query to create the table.
* *Add methods*: Add a new value to the respective tables.
* *Delete methods*: Delete the selected entry from a table.
* *Update methods*: Update the selected entry.
* *Get Single Entity Methods*: Take an entity ID an return the whole row.
* *Get Multiple Entities Methods*: Return all entries of an entity. Does not take parameters.
* *Search Methods*: Search methods by name. Case sensitive.


Fixtures Table
--------------

Fixtures table was implemented to hold the fixture data of the teams. It has *Fixture_ID* as a **primary key**, and *Season_ID* and *Team_ID* as a **foreign key**. It also has *points* data as local data.

.. code-block:: python

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS FIXTURES
                    (
                    FIXTURE_ID SERIAL NOT NULL PRIMARY KEY,
                    SEASON_ID INTEGER NOT NULL REFERENCES SEASONS(SEASON_ID),
                    TEAM_ID INTEGER NOT NULL REFERENCES TEAMS(TEAM_ID),
                    POINTS INTEGER NOT NULL
                    )
                    """)
                connection.commit()

*add_fixture* Method
^^^^^^^^^^^^^^^^^^^^
This method takes the respective queries and adds the resulting fixture to the database.
This operation is done by INSERT INTO feature in SQL. The said code is shown below.

.. code-block:: python

    def add_fixture(self, season_id, team_id, points):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO FIXTURES (SEASON_ID, TEAM_ID, POINTS) VALUES (%s, %s, %s) """
                cursor.execute(query, (season_id, team_id, points))
                connection.commit()


*delete_fixture* Method
^^^^^^^^^^^^^^^^^^^^^^^

This method takes the Fixture_ID of a query and deletes the resulting fixture from the database.
This operation is done by DELETE FROM feature in SQL. The said code is shown below.

.. code-block:: python

    def delete_fixture(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM FIXTURES
                    WHERE FIXTURE_ID = %s""",
                    id)
                connection.commit()

*update_fixture* Method
^^^^^^^^^^^^^^^^^^^^^^^

This method takes the Fixture_ID of a query and updates the said entry by simply calling the UPDATE feature in SQL.

.. code-block:: python

    def update_fixture(self, fixture_id, season_id, team_id, points):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE FIXTURES
                        SET SEASON_ID = %s,
                        TEAM_ID = %s,
                        POINTS = %s
                        WHERE FIXTURE_ID = %s"""
                cursor.execute(query, (season_id, team_id, points, fixture_id))
                connection.commit()

*search_fixture* Method
^^^^^^^^^^^^^^^^^^^^^^^

This method provides the user with all the columns related to the search query.
It runs a SELECT query with a WHERE statement to match *Fixture_ID*.
It uses JOIN feature of SQL to display the proper results.

.. code-block:: python

    def search_fixture(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT FIXTURE_ID, SEASONS.YEAR, TEAMS.NAME, POINTS
                    FROM FIXTURES
                    INNER JOIN SEASONS ON SEASONS.SEASON_ID=FIXTURES.SEASON_ID
                    INNER JOIN TEAMS ON TEAMS.TEAM_ID=FIXTURES.TEAM_ID
                    WHERE TEAMS.NAME LIKE '%s'""" % ('%'+id+'%')
            cursor.execute(query)
            connection.commit()

            result = cursor.fetchall()
            return result

*get_fixtures* Method
^^^^^^^^^^^^^^^^^^^^^

This method simply returns all the fixtures in the database. It uses LEFT JOIN feature of SQL to get **season** and **team name** data from the foreign keys.

.. code-block:: python

    def get_fixtures(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT F.FIXTURE_ID, S.YEAR, T.NAME, F.POINTS
                        FROM FIXTURES F
                        LEFT JOIN SEASONS S ON (F.SEASON_ID = S.SEASON_ID)
                        LEFT JOIN TEAMS T ON (F.TEAM_ID = T.TEAM_ID)
                        ORDER BY S.YEAR ASC"""
            cursor.execute(query)
            connection.commit()

            fixtures = [(key, season, team, points)
                        for key, season, team, points in cursor]
            return fixtures


Player Statistics Table
-----------------------

Player Statistics table was implemented to hold the various statistics data of the players in the database. It has *Statistic_ID* as a **primary key**, and *Season_ID* and *Player_ID* as a **foreign key**. It also has *tackles* and *penalties* data as local data.
The following code initializes the Team Statistics table.

.. code-block:: python

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS STATISTICSP
                    (
                    STATISTIC_ID SERIAL NOT NULL PRIMARY KEY,
                    SEASON_ID INTEGER NOT NULL REFERENCES SEASONS(SEASON_ID),
                    PLAYER_ID INTEGER NOT NULL REFERENCES PLAYERS(PLAYER_ID),
                    tackles INTEGER NOT NULL,
                    penalties INTEGER NOT NULL
                    )
                    """)
                connection.commit()

*add_statistic_player* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This method takes the respective queries and adds the resulting statistics to the database.
This operation is done by INSERT INTO feature in SQL. The said code is shown below.

.. code-block:: python

    def add_statistic_player(self, season_id, player_id, tackles, penalties):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO STATISTICSP (SEASON_ID, PLAYER_ID, tackles, penalties) VALUES (%s, %s, %s, %s) """
                cursor.execute(query, (season_id, player_id, tackles, penalties))
                connection.commit()


*delete_statistic_player* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method takes the Statistic_ID of a query and deletes the resulting statistic from the database.
This operation is done by DELETE FROM feature in SQL. The said code is shown below.

.. code-block:: python

    def delete_statistic_player(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM STATISTICSP
                    WHERE STATISTIC_ID = %s""",
                    id)
                connection.commit()

*update_statistic_player* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method takes the Statistic_ID of a query and updates the said entry by simply calling the UPDATE feature in SQL.

.. code-block:: python

    def update_statistic_player(self, statistic_id, season_id, player_id, tackles, penalties):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE STATISTICSP
                        SET SEASON_ID = %s,
                        PLAYER_ID = %s,
                        TACKLES = %s,
                        PENALTIES = %s
                        WHERE STATISTIC_ID = %s"""
                cursor.execute(query, (season_id, player_id, tackles, penalties, statistic_id))
                connection.commit()

*search_statistic_player* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method provides the user with all the columns related to the search query.
It runs a SELECT query with a WHERE statement to match *Statistic_ID*.
It uses JOIN feature of SQL to display the proper results.

.. code-block:: python

    def search_statistic_player(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT STATISTIC_ID, SEASONS.YEAR, PLAYERS.NAME, TACKLES, PENALTIES
                    FROM STATISTICSP
                    INNER JOIN SEASONS ON SEASONS.SEASON_ID=STATISTICSP.SEASON_ID
                    INNER JOIN PLAYERS ON PLAYERS.PLAYER_ID=STATISTICSP.PLAYER_ID
                    WHERE PLAYERS.NAME LIKE '%s'""" % ('%'+id+'%')
            cursor.execute(query)
            connection.commit()

            result = cursor.fetchall()
            return result

*get_statistics_player* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method simply returns all the player statistics in the database. It uses LEFT JOIN feature of SQL to get **season** and **player name** data from the foreign keys.

.. code-block:: python

    def get_statistics_player(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT S.STATISTIC_ID, SS.YEAR, P.NAME, S.TACKLES, S.PENALTIES
                        FROM STATISTICSP S
                        LEFT JOIN SEASONS SS ON (S.SEASON_ID = SS.SEASON_ID)
                        LEFT JOIN PLAYERS P ON (S.PLAYER_ID = P.PLAYER_ID)
                        ORDER BY SS.YEAR ASC"""
            cursor.execute(query)
            connection.commit()

            statisticsp = [(key, season, player, tackles, penalties)
                        for key, season, player, tackles, penalties in cursor]
            return statisticsp

Team Statistics Table
---------------------

Team Statistics table was implemented to hold the various statistics data of the teams in the database. It has *Statistic_ID* as a **primary key**, and *Season_ID* and *Team_ID* as a **foreign key**. It also has *tackles* and *penalties* data as local data.
The following code initializes the Team Statistics table.

.. code-block:: python

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS STATISTICST
                    (
                    STATISTIC_ID SERIAL NOT NULL PRIMARY KEY,
                    SEASON_ID INTEGER NOT NULL REFERENCES SEASONS(SEASON_ID),
                    TEAM_ID INTEGER NOT NULL REFERENCES TEAMS(TEAM_ID),
                    touchdowns INTEGER NOT NULL,
                    rushingYards INTEGER NOT NULL
                    )
                    """)
                connection.commit()


*add_statistic_team* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^
This method takes the respective queries and adds the resulting statistics to the database.
This operation is done by INSERT INTO feature in SQL. The said code is shown below.

.. code-block:: python

    def add_statistic_team(self, season_id, team_id, touchdowns, rushingYards):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO STATISTICST (SEASON_ID, TEAM_ID, touchdowns, rushingYards) VALUES (%s, %s, %s, %s) """
                cursor.execute(query, (season_id, team_id, touchdowns, rushingYards))
                connection.commit()


*delete_statistic_team* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method takes the Statistic_ID of a query and deletes the resulting statistic from the database.
This operation is done by DELETE FROM feature in SQL. The said code is shown below.

.. code-block:: python

    def delete_statistic_team(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM STATISTICST
                    WHERE STATISTIC_ID = %s""",
                    id)
                connection.commit()

*update_statistic_team* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method takes the Statistic_ID of a query and updates the said entry by simply calling the UPDATE feature in SQL.

.. code-block:: python

    def update_statistic_team(self, statistic_id, season_id, team_id, touchdowns, rushingYards):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE STATISTICST
                        SET SEASON_ID = %s,
                        TEAM_ID = %s,
                        TOUCHDOWNS = %s,
                        RUSHINGYARDS = %s
                        WHERE STATISTIC_ID = %s"""
                cursor.execute(query, (season_id, team_id, touchdowns, rushingYards, statistic_id))
                connection.commit()

*search_statistic_team* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method provides the user with all the columns related to the search query.
It runs a SELECT query with a WHERE statement to match *Statistic_ID*.
It uses JOIN feature of SQL to display the proper results.

.. code-block:: python

    def search_statistic_team(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT STATISTIC_ID, SEASONS.YEAR, TEAMS.NAME, TOUCHDOWNS, RUSHINGYARDS
                    FROM STATISTICST
                    INNER JOIN SEASONS ON SEASONS.SEASON_ID=STATISTICST.SEASON_ID
                    INNER JOIN TEAMS ON TEAMS.TEAM_ID=STATISTICST.TEAM_ID
                    WHERE TEAMS.NAME LIKE '%s'""" % ('%'+id+'%')
            cursor.execute(query)
            connection.commit()

            result = cursor.fetchall()
            return result

*get_statistics_team* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method simply returns all the team statistics in the database. It uses LEFT JOIN feature of SQL to get **season** and **team name** data from the foreign keys.

.. code-block:: python

    def get_statistics_team(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT S.STATISTIC_ID, SS.YEAR, T.NAME, S.TOUCHDOWNS, S.RUSHINGYARDS
                        FROM STATISTICST S
                        LEFT JOIN SEASONS SS ON (S.SEASON_ID = SS.SEASON_ID)
                        LEFT JOIN TEAMS T ON (S.TEAM_ID = T.TEAM_ID)
                        ORDER BY SS.YEAR ASC"""
            cursor.execute(query)
            connection.commit()

            statisticst = [(key, season, team, touchdowns, rushingYards)
                        for key, season, team, touchdowns, rushingYards in cursor]
            return statisticst
