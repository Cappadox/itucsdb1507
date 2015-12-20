Parts Implemented by Sefa Eren Şahin
====================================

**Players, Teams and Squad tables are implemented.**

Players Table
-------------
This table consists of 4 columns::

| Column Name   | Data Type | Key         |
| ------------- |:---------:| -----------:|
| PLAYER_ID     | serial    | PRIMARY KEY |
| NAME          | varchar   | none        |
| BIRTHDAY      | date      | none        |
| POSITION      | varchar   | none        |

*Table Initialization*
----------------------

Table is created by following sql code::

   CREATE TABLE IF NOT EXISTS PLAYERS
                       ( PLAYER_ID serial NOT NULL PRIMARY KEY,
                         NAME varchar(100) NOT NULL,
                         BIRTHDAY date NOT NULL,
                         POSITION varchar(100) NOT NULL
                       )

*Selection*
-----------

If "//players" route is loaded by GET method, players are going to be selected and will be printed to players.html::

   @app.route('/players', methods=['GET', 'POST'])
   def players():
       if request.method == 'GET':
           return render_template('players.html', players = app.players.select_players())
       else:
           name = request.form['name']
           birthday = request.form['birthday']
           position = request.form['position']
           app.players.add_player(name, birthday, position)
       return redirect(url_for('players'))

Selection operation is done by the following function which is in players.py::

   def select_players(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM PLAYERS ORDER BY PLAYER_ID"""
             cursor.execute(query)
             players = cursor.fetchall()
             return players

*Insert Operation*
------------------

A route is defined in order to use Player Adding html page::

   @app.route('/players/add', methods=['GET', 'POST'])
   def add_players():
    return render_template('players_add.html')

After the form is filled and submitted in page, form action directs to the following route::

   @app.route('/players', methods=['GET', 'POST'])
   def players():
       if request.method == 'GET':
           return render_template('players.html', players = app.players.select_players())
       else:
           name = request.form['name']
           birthday = request.form['birthday']
           position = request.form['position']
           app.players.add_player(name, birthday, position)
       return redirect(url_for('players'))

If "//players" route is loaded by POST method, which is the player addition form's method, player will be added and route will redirect to itself again.
If route is loaded by GET method, players.html page will be opened up.

Insertion operation is done by the following function which is in players.py::

   def add_player(self, name, birthday, position):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO PLAYERS (NAME, BIRTHDAY, POSITION) VALUES (%s, %s, %s) """
                cursor.execute(query, (name, birthday, position))
                connection.commit()

*Update Operation*
------------------

In update operation, route is defined uniquely for the corresponding tuple's player_id.::

   @app.route('/players/update/<player_id>', methods=['GET', 'POST'])
   def update_players(player_id):
       if request.method == 'GET':
           return render_template('players_edit.html', player = app.players.get_player(player_id))
       else:
           name = request.form['name']
           birthday = request.form['birthday']
           position = request.form['position']
           app.players.update_player(player_id, name, birthday, position)
           return redirect(url_for('players'))

If the route is loaded by GET method, player with corresponding player_id will be selected to update and route will be directed to players_edit.html::

   def get_player(self, player_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM PLAYERS WHERE PLAYER_ID = %s """
             cursor.execute(query, [player_id])
             player = cursor.fetchall()
             return player

The form's action in players_edit.html redirects form to the current route. Since form's method is POST, route is loaded by POST method.
Values are requested from form and the update function is called. After that, route redirects to players page.
Update operation is done by the following function in players.py::

   def update_player(self, player_id, name, birthday, position):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE PLAYERS
                        SET NAME = %s,
                        BIRTHDAY = %s,
                        POSITION = %s
                        WHERE
                        PLAYER_ID = %s """
                cursor.execute(query, (name, birthday, position, player_id))
                connection.commit()

*Delete Operation*
------------------

Delete operation is very similar to Update operation. Like update, in delete operation, route is defined uniquely for the corresponding tuple's player id.::

   @app.route('/players/delete/<player_id>', methods=['GET', 'POST'])
   def delete_players(player_id):
       app.players.delete_player(player_id)
       return redirect(url_for('players'))

After the player is deleted, route redirects to players page. Delete operation is done by the following function in players.py::

   def delete_player(self, player_id):
         with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ DELETE FROM PLAYERS
                        WHERE PLAYER_ID = %s """
                cursor.execute(query, [player_id])
                connection.commit()

*Search Operation*
------------------

A route is defined in order to search players by player name. Search form is in players.html::

   @app.route('/players/search', methods = ['GET', 'POST'])
   def search_players():
    if request.method == 'GET':
        return redirect(url_for('players_search.html'))
    else:
        searchname = request.form['nametosearch']
        return render_template('players_search.html', players = app.players.search_player(searchname))

Since the form has POST method, after the submission, search name will be requested from form. After searching, results will be listed in players_search.html.

Searching is done by the following function in players.py::

   def search_player(self, name):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ SELECT * FROM PLAYERS WHERE NAME LIKE %s ORDER BY PLAYER_ID """
                cursor.execute(query, ['%'+name+'%'])
                players = cursor.fetchall()
                return players

