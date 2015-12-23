Parts Implemented by Kubilay Karpat
===================================
I implemented country, league and stadium entities and belonging operations. I created countries, leagues and stadiums classes in order to implement demanded operations. All these classes contains same basic methods which listed below.

* Initialize table methods
   This operations basicly run a queary to create related table.
* Add methods
   This methods take variables that represent columns in table and perform a insert operation.
* Delete methods
   This method takes the entity's primary key and delete it from database. Users reach delete function from listing pages and they do not naturally interact with the primary keys, this information kept but hidden.
* Update methods
   Similar with add methods this methods also take entitys fields as parameters but also an entity ID which corresponds to the primary key in the table is given. Same as in the delete operation, these keys are invisible to users.
* Get Entity Methods
   These methods take an entity ID an returns the entities all columns. These are actually helper functions that used by another entities since some table have foreing keys and had to reach related name or etc with these keys.
* Get Entities Methods
   Mostly used in list pages these methods simply returns all entries belong to a entity. Also these functions used in to Add / Delete operations of entities that have foreing keys since they need to list all options to the users as a dropdown etc. These methods do not take parameters.
* Search Methods
   Search methods designed to search by name in all three entities as case sensitive. They basically takes a string that represents search words and returns all related entries.

Delete and Update Operations and Their Form
-------------------------------------------
I want to implement delete and update functions in list page in a such way that users can easily reach. In order to archive this I placed delete and update buttons following the entries in list page.

   .. figure:: images/member3/update_delete_button.png
      :scale: 100 %

      Users can directly delete entries or reach their update pages.

In delete button I used a hidden form value to send the primary key with POST request.
But in update button I just put the ID of element that want to deleted in to URL.
In this way I achieved the function that I want, users were able to delete / update entries by just clicking the corresponding button without entering a key value or an attribute like name etc.

.. code-block:: html

      <form action="{{ url_for('countries') }}" method="post" role="form" style="display: inline">
         <input value="{{key}}" name="id" type="hidden" />
         <button class="btn btn-primary btn-sm" name="Delete" type="submit"><span class="glyphicon glyphicon-trash" ></button>
      </form>
      <form action="{{url_for('country_edit', country_id=key )}}" method="get" role="form" style="display: inline">
         <button class="btn btn-primary btn-sm" name="Update" type="submit"><span class="glyphicon glyphicon-wrench" ></button>
      </form>



Country Implementation
----------------------
I designed countries class in order to perform operations in my countries table. Country is a core entity in our dateabase and used in some tables as a foreing key. Also ı designed a country class to represent a row data of a country except for primary key.

.. note:: After implementing country entity and some of league functions I realized that using a class for holding entity information and using it as a parameter in functions is not a good way to maintain the operations. In other entities I did not used classes for entities / methods instead I used column variables as seperate parameters.
Countires Table
^^^^^^^^^^^^^^^
In our database countries table has following columns

* *COUNTRY_ID* as **serial** type and primary key
   This is the primary key of the table
* *NAME* as **varchar(50)** and not null
   This column holds the name of the country and it can't be null
* *ABBREVIATION* a **varchar(5)**
   This column holds the abbrevitaion of the country (like US, UK etc.)

Since this is a core entity, it does not has a foreing key.

*add_country* Method
^^^^^^^^^^^^^^^^^^^^
This method takes a country object as a parameter and insert it into database.

Here is the code block that does the add operation in database using INSERT command:

.. code-block:: python

   def add_country(self, country):
      with dbapi2.connect(self.app.config['dsn']) as connection:
                   cursor = connection.cursor()
                   cursor.execute("""
                       INSERT INTO COUNTRIES (NAME, ABBREVIATION)
                       VALUES (%s, %s) """, (country.name,country. abbreviation))
                   connection.commit()


*delete_country* Method
^^^^^^^^^^^^^^^^^^^^^^^

This method takes a country id (which is a primary key of countries table actually) and deletes if from database. To match the country on database *WHERE* statement used on country id column.

Here is the code block that perform delete operation on countries table.

.. code-block:: python

   def delete_country(self, id):
      with dbapi2.connect(self.app.config['dsn']) as connection:
          cursor = connection.cursor()
          query = """ DELETE FROM COUNTRIES WHERE COUNTRY_ID =%s """
          cursor.execute(query, [id])
          connection.commit()

*update_country* Method
^^^^^^^^^^^^^^^^^^^^^^^
This method works in a similar fashion with add function, it takes one more argument which is the *country id*. The given *Country* object is parsed and the row that related with country id argument is updated with tihs parsed information.

.. code-block:: python

   def update_country(self, country_id, country):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE COUNTRIES
                                SET NAME = %s, ABBREVIATION = %s
                            WHERE COUNTRY_ID = %s """
                cursor.execute(query, (country.name,country. abbreviation,country_id ))
                connection.commit()

*get_country* Method
^^^^^^^^^^^^^^^^^^^^
 This method is used by another classes. It is main function is the provide all columns related with a foreing key which consists a *country id*. It does simply run *SELECT* query with *WHERE* statement to match *country id*.

.. code-block:: python

   def get_country(self, id):
      with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM COUNTRIES WHERE COUNTRY_ID =%s """
             cursor.execute(query, [id])

             connection.commit()
             result = cursor.fetchone()
             country = Country(result[1], result[2])
             return country

*get_countries Method*
^^^^^^^^^^^^^^^^^^^^^^
Similiar to *get_country* methods runs a *SELECT* on countries table but this time without a specific ID. Simply it returns all countries in database without taking a parameter.

.. code-block:: python

    def get_countries(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM COUNTRIES ORDER BY NAME"""
            cursor.execute(query)
            connection.commit()
            countries = [(key, Country(name, abbreviation))
                        for key, name, abbreviation in cursor]

            return countries


*search_countries Method*
^^^^^^^^^^^^^^^^^^^^^^^^^
This method takes a string and search in countires table by matching this string which is the search pharase acutally on the name column and returns a list of matching countries.


.. code-block:: python

    def search_countries(self, search_terms):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM COUNTRIES WHERE NAME LIKE '%s' ORDER BY NAME""" % (('%'+search_terms+'%'))
            cursor.execute(query)
            connection.commit()
            countries = [(key, Country(name, abbreviation))
                        for key, name, abbreviation in cursor]
            return countries

League Implementation
---------------------
League is an important entity in American Football Database project because all the teams, matches, coaches, officals are specific for a league.

Leagues Table
^^^^^^^^^^^^^
Leagues table consists of following columns:

* *LEAGUE_ID* as **serial** type and primary key
   This is the primary key of the table
* *NAME* as **varchar(100)** and not null
   This column holds the name of the league and it can't be null
* *ABBREVIATION* a **varchar(10)**
   This column holds the abbrevitaion of the leaguey (like NFL)
* *COUNTRY_ID* as **integer** type, nut null and references to countries table
   This is foreing key to countries table, represent the country that the leauge has belongs to

*add_league* Method
^^^^^^^^^^^^^^^^^^^
This method takes a league object and performs *INSERT* operation onto database.

.. code-block:: python

    def add_league(self, league):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO LEAGUES (NAME, ABBREVIATION, COUNTRY_ID)
                    VALUES (%s, %s, %s) """,
                    (league.name, league.abbreviation, league.countryID))
                connection.commit()

*delete_league Method*
^^^^^^^^^^^^^^^^^^^^^^
This method takes a *league_id* and deletes corresponding row from database using *DELETE* operation.

.. code-block:: python

    def delete_league(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ DELETE FROM LEAGUES WHERE LEAGUE_ID =%s """
                cursor.execute(query, [id])
                connection.commit()

*update_league* Method
^^^^^^^^^^^^^^^^^^^^^^
Takes an *league_id* and match the row in database then updates all columns with given parameters.

.. code-block:: python

    def update_league(self, league_id, name, abbreviation, country_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE LEAGUES
                                SET NAME = %s, ABBREVIATION = %s, COUNTRY_ID = %s
                            WHERE LEAGUE_ID = %s """
                cursor.execute(query, (name, abbreviation, country_id, league_id))
                connection.commit()

*get_league* Method
^^^^^^^^^^^^^^^^^^^
This method is an helper function to other entities which hold *league_id* as a foreing key. It simply takes an *league_id* and returns corresponding league information.

.. code-block:: python

    def get_league(self, league_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM LEAGUES
                        WHERE LEAGUE_ID =%s """
            cursor.execute(query, [league_id])
            connection.commit()

            league_id, name, abbreviation, country_id = cursor.fetchone()
            return league_id, name, abbreviation, country_id

*get_leagues* Method
^^^^^^^^^^^^^^^^^^^^
This method used to fetch all leagues from the database. It does not take a parameter and as a return value it returns the list of leagues information in the database.

.. code-block:: python

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

*search_leagues* Method
^^^^^^^^^^^^^^^^^^^^^^^
Search countries method runs a *SELECT* argument with *WHERE* argument which compare the given input parameter with leagues' names with *LIKE* option. The results returned as a list.

.. code-block:: python

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