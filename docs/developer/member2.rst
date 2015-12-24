Parts Implemented by İlay Köksal
================================
I created coaches, seasons and coaching tables and their operations. All these tables contains same operations like Add, Delete, Update and Search.

* Initialize Table
   Creation of the table.
* Select
   Returns all elements of table
* Get
   Makes inner join to select wanted colums from other tables. Basicly used in tables in which cocsists foreign key.
* Add
   Adding new row to table
* Delete
   Deleting row from table
* Update
   Updating selected row
* Search
   Searching table with given condition and returning rows which verify search condition.

Coaches Table and Operations
----------------------------
First i created a coaches class to implement all related operations for Coaches table.

Coaches table has the fallowing columns

* *COACH_ID* as serial primary key
   This is the primary key of the table
* *NAME* as varchar(50) and not null
   Holds the name of the coach and can not be null
* *BIRTHDAY* as integer and not null
   Birthyear of coach.

Coaches table is a core table so it does not have any foreign key.

*initialize_tables*
^^^^^^^^^^^^^^^^^^^
First we create table with *CREATE* sql statement.

.. code-block:: python

   def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS COACHES
                (
                COACH_ID SERIAL PRIMARY KEY,
                NAME VARCHAR(50) NOT NULL,
                BIRTHDAY INTEGER NOT NULL
                ) """)
                connection.commit()

*select_coaches*
^^^^^^^^^^^^^^^^
With this method, we can see every coach item in table in ascending order.

.. code-block:: python

   def select_coaches(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM COACHES ORDER BY COACH_ID ASC"""
             cursor.execute(query)
             result = cursor.fetchall()
             return result


*add_coach*
^^^^^^^^^^^

This function takes name and birthday and add them to database with *INSERT* satatement.

.. code-block:: python

   def add_coach(self, name, birthday):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO COACHES (NAME, BIRTHDAY) VALUES (%s, %s) """
                cursor.execute(query, (name, birthday))
                connection.commit()

*seach_coach*
^^^^^^^^^^^^^
This method returns the matching coaches to given string with *WHERE* and *SELECT* statements.

.. code-block:: python

   def search_coach(self, name):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query="""SELECT * FROM COACHES c WHERE c.NAME LIKE '%s'"""% (('%'+name+'%'))
                cursor.execute(query)
                connection.commit()
                result = [(key, name,birth)
                        for key, name,birth in cursor]
                return result

*delete_coach*
^^^^^^^^^^^^^^
Deleting done with taking the id of item that we want to delete and using it in *DELETE* and *WHERE* query.

.. code-block:: python

   def delete_coach(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ DELETE FROM COACHES WHERE COACH_ID =%s """
                cursor.execute(query, [id])
                connection.commit()

*update_coach*
^^^^^^^^^^^^^^
Works similar to add function but in addition takes id argument of the item that we want to update.

.. code-block:: python

    def update_coach(self, coach_id, name, birthday):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE COACHES SET NAME = %s, BIRTHDAY= %s WHERE COACH_ID = %s """
                cursor.execute(query, (name,birthday,coach_id))
                connection.commit()



Seasons Table and Operations
----------------------------
Seasons table class created first to write its operations.

This table has columns below.

* *SEASON_ID* as serial primary key
   This is the primary key of the table
* *YEAR* as integer and not null
   Year value of season.

Seasons table is a core table as well so it does not have any foreign key too.

*initialize_tables*
^^^^^^^^^^^^^^^^^^^
First we create table with *CREATE* sql statement.

.. code-block:: python

   def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS SEASONS
                (
                SEASON_ID SERIAL PRIMARY KEY,
                YEAR INTEGER NOT NULL
                ) """)
                connection.commit()

*select_seasons*
^^^^^^^^^^^^^^^^
With this method, we can see every season value in ascending order.

.. code-block:: python

   def select_seasons(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM SEASONS ORDER BY SEASON_ID ASC"""
             cursor.execute(query)
             result = cursor.fetchall()
             return result

*get_season*
^^^^^^^^^^^^
This method used by other classes and tables. They use this to select season with season id.

.. code-block:: python

   def get_season(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM SEASONS
                         WHERE SEASON_ID = %s"""
             cursor.execute(query,[id])
             season_id,year = cursor.fetchone()
             return year


*add_season*
^^^^^^^^^^^^

This function takes year value and add it to database with *INSERT* sql satatement.

.. code-block:: python

   def add_season(self, year):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO SEASONS (year) VALUES (%s) """
                cursor.execute(query, [year])
                connection.commit()

*seach_coach*
^^^^^^^^^^^^^
This method returns the matching season with *WHERE* and *SELECT* statements.

.. code-block:: python

   def search_season(self, year1):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query="""SELECT * FROM SEASONS WHERE YEAR = %s"""
             cursor.execute(query,[year1])
             connection.commit()
             result = [(key, year)
                        for key, year in cursor]
             return result

*delete_season*
^^^^^^^^^^^^^^^
Method takes id of the item as parameter. With *WHERE* statement, we can delete related item.

.. code-block:: python

   def delete_season(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ DELETE FROM SEASONS WHERE SEASON_ID =%s """
                cursor.execute(query, [id])
                connection.commit()

*update_coach*
^^^^^^^^^^^^^^
Similar to add function but in addition takes id value of the item to be updated.

.. code-block:: python

   def update_season(self, season_id, year):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE SEASONS SET YEAR = %s WHERE SEASON_ID = %s """
                cursor.execute(query, (year,season_id))
                connection.commit()


Coaching Table and Operations
-----------------------------
Coaching table class created and its operations implemented.

This table has columns below.

* *COACHING_ID* as serial primary key
   This is the primary key of the table
* *TEAM_ID* as integer and not null and references TEAM table
* *COACH_ID* as integer and not null and references COACHES table
* *SEASON_ID* as integer and not null and references SEASONS table


Coaching table is a relation table. It has three foreign keys and one serial primary key.

*initialize_tables*
^^^^^^^^^^^^^^^^^^^
First we create table with *CREATE* sql statement.

.. code-block:: python

   def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS COACHING
                (
                COACHING_ID SERIAL NOT NULL PRIMARY KEY,
                TEAM_ID INT NOT NULL REFERENCES TEAMS(TEAM_ID),
                COACH_ID INT NOT NULL REFERENCES COACHES(COACH_ID),
                SEASON_ID INT NOT NULL REFERENCES SEASONS(SEASON_ID)
                ) """)
                connection.commit()
*select_coaching*
^^^^^^^^^^^^^^^^^
This method helps us to see every coaching relation we have in our database.

.. code-block:: python

   def select_coaching(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """SELECT * FROM COACHING"""
             cursor.execute(query)
             result = cursor.fetchall()
             return result

*get_coaching*
^^^^^^^^^^^^^^
With this method we call the values from other tables to show.

.. code-block:: python

   def get_coaching(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ select coaching_id, teams.name, coaches.name, seasons.year
                    from coaching
                    inner join teams on teams.team_id=coaching.team_id
                    inner join coaches on coaches.coach_id=coaching.coach_id
                    inner join seasons on seasons.season_id=coaching.season_id"""
             cursor.execute(query)
             result = cursor.fetchall()
             return result

*add_coaching*
^^^^^^^^^^^^^^

This function takes Team id, Season id and Coach id and add them to database with *INSERT* sql statement.

.. code-block:: python

   def add_coaching(self,team_id,coach_id,season_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO COACHING (TEAM_ID, COACH_ID, SEASON_ID) VALUES (%s, %s, %s) """
                cursor.execute(query, (team_id, coach_id, season_id))
                connection.commit()

*seach_coaching*
^^^^^^^^^^^^^^^^
This method returns the matching coaching row with *WHERE* and *SELECT* statements.


.. code-block:: python

   def search_coaching(self, term):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""select coaching_id, teams.name, coaches.name, seasons.year
                    from coaching
                    inner join teams on teams.team_id=coaching.team_id
                    inner join coaches on coaches.coach_id=coaching.coach_id
                    inner join seasons on seasons.season_id=coaching.season_id
                    WHERE coaches.name LIKE '%s' OR teams.name LIKE '%s'""" % (('%'+term+'%'),('%'+term+'%'))
            cursor.execute(query)
            connection.commit()
            coachlist = [(key, team, name, year)
                        for key, team, name, year in cursor]

            return coachlist


*delete_coaching*
^^^^^^^^^^^^^^^^^
Method takes id of the item as parameter. With *WHERE* statement it finds item that we want to delete.

.. code-block:: python

   def delete_coaching(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor=connection.cursor()
                query ="""
                    DELETE FROM COACHING
                    WHERE COACHING_ID = %s"""
                cursor.execute(query,[id])
                connection.commit()

*update_coaching*
^^^^^^^^^^^^^^^^^
Like add function but in addition takes id value of the row to update.

.. code-block:: python

   def update_coaching(self, coaching_id, team_id, coach_id, season_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE COACHING
                        SET TEAM_ID = %s,
                        COACH_ID = %s,
                        SEASON_ID = %s
                        WHERE COACHING_ID = %s"""
                cursor.execute(query, [team_id, coach_id, season_id, coaching_id])
                connection.commit()
