Parts Implemented by Alparslan Tozan
====================================
I implemented official, match and transfer entities and belonging operations.
In order to do that I created officials, matches and transfers classes to implement demanded operations.

All these classes contains same basic methods which listed below.

Operations
----------
* Initialize table methods
   This operations basicly run a queary to create related table.
* Add methods
   This methods take variables that represent columns in table and perform a insert operation.
* Delete methods
   This method takes the entity's primary key and delete it from database. Users reach delete function from listing pages and they do not naturally interact with the primary keys, this information kept but hidden.
* Update methods
   Similar with add methods this methods also take entitys fields as parameters but also an entity ID which corresponds to the primary key in the table is given. Same as in the delete operation, these keys are invisible to users.
* Get Entity Method [#f1]_
   These methods take an entity ID an returns the entity's all columns. These are actually helper functions that used by another entities since some table have foreing keys and had to reach related name or etc with these keys.
* Get Entities Methods
   Mostly used in list pages these methods simply returns all entries belong to a entity. Also these functions used in to Add / Delete operations of entities that have foreing keys since they need to list all options to the users as a dropdown etc. These methods do not take parameters.
* Search Method [#f2]_
   Search method designed to search by name or age in official entity as case sensitive. It basically takes a string or a number, which will later be changed into a string, that represents search words and returns all related entities.

Delete and Update Operations and Their Form
-------------------------------------------
I want to implement delete and update functions in list page in a such way that users can easily reach. In order to archive this I placed delete and update buttons following the entries in list page.

   .. figure:: images/member1/checkbox.png
      :scale: 100 %

      User need to select one of the check boxes.

   .. figure:: images/member1/delete_update_buttons.png
      :scale: 100 %

      After selecting one of the check boxes user can determine between update and delete operations

In check boxes I used a hidden form value to send the primary key with POST request.
Forms action is posting these values to a determination page, which will determine the process.
After check boxes i putted another hidden value. If none of the check boxes is selected but update/delete button is still selected, with this value we make sure there will not be an error from web site.
In this way I achieved the function that I want, users were able to delete / update entries by just checking the corresponding check box without entering a key value or an attribute like name etc.

HTML Part
^^^^^^^^^

.. code-block:: html

      <form action="{{ url_for('transfer_add') }}" method="post" role="form">
      ...
         {% for key, transfer in transfers %}
         ...
            <td><input type="checkbox" name="id" value="{{ key }}"/></td>
         </tr>
         {% endfor %}
      </table>
         <input type="hidden" value="0" name="id">
         <div class="col-sm-10">
            <input type="submit" value="Delete" name ="submit">
            <input type="submit" value="Update" name ="submit">
         </div>
      </form>

Python Part
^^^^^^^^^^^

.. code-block:: python

   def transfer_determine():
      if request.method=='GET':
         return redirect(url_for('transfers'))
      if request.form['id']=="0":
         return redirect(url_for('transfers'))
      if request.form['submit'] == "Delete":
         id = request.form['id']
         form = request.form
         form_data={id: form['id']}
         return redirect(url_for('transfer_delete'), code=307 )
      elif request.form['submit'] == "Update":
         return render_template('transfer_update.html', id = request.form['id'], teams=app.teams.select_teams(),
                             season=app.seasons.select_seasons(),players=app.players.select_players())
      else:
         return redirect(url_for('transfers'))

Official Implementation
-----------------------
I designed officials class in order to perform operations in my officials table. Official is a core entity in our database and used in matches tables as a foreing key. Also I designed a official class to represent a row data of a country except for primary key.

.. note:: After implementing official entity and some of matches functions I realized that using a class for holding entity information and
          using it as a parameter in functions is not a good way to maintain the operations. In other entities I did not used classes for
          entities / methods instead I used column variables as seperate parameters.
Officials Table
^^^^^^^^^^^^^^^
In our database countries table has following columns

* *OFFICIAL_ID* as **serial** type and primary key
   *This is the primary key of the table*
* *NAME* as **varchar(100)** and not null
   *This column holds the full name of the official and it can't be null*
* *AGE* as **INT** and not null
   *This column holds the age of the official*

Since this is a core entity, it does not has a foreing key.

*add_official* Method
^^^^^^^^^^^^^^^^^^^^^
This method takes a official object as a parameter and insert it into database.

Here is the code block that does the add operation in database using **INSERT** command:

.. code-block:: python

   def add_official(self, name, age):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO OFFICIALS (NAME, AGE)
                    VALUES (%s, %s) """,
                    (name, age))
                connection.commit()


*delete_official* Method
^^^^^^^^^^^^^^^^^^^^^^^^

This method takes a *official_id* (which is a primary key of officials table) and deletes if from database.
To match the country on database *WHERE* statement used on *official_id* column.

Here is the code block that perform delete operation on officials table using **DELETE** command:

.. code-block:: python

   def delete_official(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM OFFICIALS
                    WHERE OFFICIAL_ID = %s""",
                    id)
                connection.commit()

*update_official* Method
^^^^^^^^^^^^^^^^^^^^^^^^
This method works in a similar fashion with add function, it takes one more argument which is the *official_id*.
The given *Official* object is parsed and the row that related with *official_id* argument is updated with this parsed information.

Here is the code block that perform update operation on officials table using **UPDATE** command:

.. code-block:: python

   def update_official(self, id, official):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE OFFICIALS
                        SET NAME = %s, AGE = %s
                        WHERE OFFICIAL_ID = %s"""
                cursor.execute(query, (official.name, official.age, id))
                connection.commit()

*get_official* Method
^^^^^^^^^^^^^^^^^^^^^
 This method is used by matches class. It is main function is the provide all columns related with a foreing key which consists a *official_id*.
 It does simply run *SELECT* query with *WHERE* statement to match *official_id*.
 It just returns the *name* of the matching id.

.. code-block:: python

   def get_official(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query="""SELECT * FROM OFFICIALS WHERE OFFICIAL_ID = %s"""
                cursor.execute(query, [id])
                key,name,age = cursor.fetchone();
                return name

*get_officials Method*
^^^^^^^^^^^^^^^^^^^^^^
Similiar to *get_country* methods runs a *SELECT* on countries table but this time without a specific ID.
Simply it returns all officials in database without taking a parameter.

.. code-block:: python

    def get_officials(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM OFFICIALS
                        ORDER BY OFFICIAL_ID ASC"""
            cursor.execute(query)
            connection.commit()

            officials = [(key, Official(name, age))
                        for key, name, age in cursor]

            return officials


*search_officials Method*
^^^^^^^^^^^^^^^^^^^^^^^^^
This method takes two string values to search in officials table by matching this strings which is the search pharase acutally on the name and age columns and returns a list of matching officials.


.. code-block:: python

    def search_officials(self, name, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM OFFICIALS
                    WHERE NAME LIKE '%s' AND CAST(AGE as VARCHAR(30)) LIKE '%s'
                    ORDER BY OFFICIAL_ID ASC""" % (('%'+name+'%','%'+id+'%'))
            cursor.execute(query)
            connection.commit()
            print(name)

            officials = [(key, Official(name, age))
                        for key, name, age in cursor]

            return officials

Match Implementation
--------------------
Match is an important entity in American Football Database project that stores all matches that had been played.

Matches Table
^^^^^^^^^^^^^
Matches table consists of following columns:

* *MATCH_ID* as **serial** type and primary key
   *This is the primary key of the table*
* *SEASON_ID* as **integer** type, not null and references to seasons table
   *This is foreing key to seasons table, represent the season that the match has been played at*
* *HOME_ID* as **integer** type, not null and references to teams table
   *This is foreing key to teams table, represent the home team that played match*
* *VISITOR_ID* as **integer** type, not null and references to countries table
   *This is foreing key to teams table, represent the away team that played match*
* *OFFICIAL_ID* as **integer** type and references to officials table
   *This is foreing key to officials table, represent the official that monitored the match*
* *RESULT* as **varchar(30)** and not null
   *This column holds the result of the match and it cannot be null*

*add_match* Method
^^^^^^^^^^^^^^^^^^
This method takes a match object and performs *INSERT* operation onto database.

.. code-block:: python

    def add_match(self, match):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO MATCHES (SEASON_ID, HOME_ID, VISITOR_ID, OFFICIAL_ID, RESULT)
                    VALUES (%s, %s, %s, %s, %s) """,
                    (match.season_id, match.home_id, match.away_id, match.official_id, match.result))
                connection.commit()

*delete_match Method*
^^^^^^^^^^^^^^^^^^^^^
This method takes a *match_id* and deletes corresponding row from database using *DELETE* operation.

.. code-block:: python

    def delete_match(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM MATCHES
                    WHERE MATCH_ID = %s""",
                    id)
                connection.commit()

*update_match* Method
^^^^^^^^^^^^^^^^^^^^^
Takes an *match_id* and match the row in database then updates all columns with given parameters.

.. code-block:: python

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

*get_matches* Method
^^^^^^^^^^^^^^^^^^^^
This method used to fetch all matches from the database. It does not take a parameter and as a return value it returns the list of matches information in the database.

.. code-block:: python

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

.. note:: *MATCHES* table holds various informations where these informations located by referencing other tables.
          To make our listing more understandable we get names of these informations using basic get functions using ID's of these tables.

Transfer Implementation
-----------------------
Transfer is a small entity that used to store records of transfers.

.. note:: We first planned to give a reference to transfer in *MATCHES* table but we could not able to implement time due to lack of time.

Transfer Table
^^^^^^^^^^^^^^
Transfer table consists of following columns:

* *TRANSFER_ID* as **serial** type and primary key
   *This is the primary key of the table*
* *SEASON_ID* as **integer** type, not null and references to seasons table
   *This is foreing key to seasons table, represent the season that the transfer has took place*
* *OLD_ID* as **integer** type, not null and references to teams table
   *This is foreing key to teams table, represent the team that player played before transfer*
* *NEW_ID* as **integer** type, not null and references to countries table
   *This is foreing key to teams table, represent the team that player is played after transfer*
* *PLAYER_ID* as **integer** type and references to players table
   *This is foreing key to players table, represent the player that transfered*
* *FEE* as **varchar(30)** and not null
   *This column holds the fee of the transfer and it cannot be null*


*add_transfer* Method
^^^^^^^^^^^^^^^^^^^^^
This method takes a transfer object and performs *INSERT* operation on *TRANSFERS* table.

.. code-block:: python

    def add_transfer(self, transfer):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO TRANSFERS (SEASON_ID, OLD_ID, NEW_ID, PLAYER_ID, FEE)
                    VALUES (%s, %s, %s, %s, %s) """,
                    (transfer.season_id, transfer.old_id, transfer.new_id, transfer.player_id, transfer.fee))
                connection.commit()

*delete_transfer* Method
^^^^^^^^^^^^^^^^^^^^^^^^
This method takes an *transfer_id* and deletes corresponding row from database.

.. code-block:: python

       def delete_transfer(self, id):
         with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM TRANSFERS
                    WHERE TRANSFER_ID = %s""",
                    id)
                connection.commit()

*update_transfer* Method
^^^^^^^^^^^^^^^^^^^^^^^^
This method takes an *transfer_id* and new information that belongs to this entry as transfer object.

.. code-block:: python

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

*get_transfers* Method
^^^^^^^^^^^^^^^^^^^^^^
This method returns all transfers and information belongs to that transfers by using fetchall function and **JOIN** operations.

.. code-block:: python

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

.. note:: Even though get functions of *MATCHES* and *TRANSFERS* tables works same, one gets its entries names from basic functions,
         other gets these values from join operations. As join operation returns only the result that we want, we can say it is more effective.

.. rubric:: Footnotes

.. [#f1] Only in Officials
.. [#f2] Only in Officials