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
^^^^^^^^^^^^^^^^^^^^^^

Table is created by following sql code::

   CREATE TABLE IF NOT EXISTS PLAYERS
                       ( PLAYER_ID serial NOT NULL PRIMARY KEY,
                         NAME varchar(100) NOT NULL,
                         BIRTHDAY date NOT NULL,
                         POSITION varchar(100) NOT NULL
                       )

*Selection*
^^^^^^^^^^^

If "/players" route is loaded by GET method, players are going to be selected and will be printed to players.html::

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
^^^^^^^^^^^^^^^^^^

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

If "/players" route is loaded by POST method, which is the player addition form's method, player will be added and route will redirect to itself again.
If route is loaded by GET method, players.html page will be opened up.

Insertion operation is done by the following function which is in players.py::

   def add_player(self, name, birthday, position):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO PLAYERS (NAME, BIRTHDAY, POSITION) VALUES (%s, %s, %s) """
                cursor.execute(query, (name, birthday, position))
                connection.commit()

*Update Operation*
^^^^^^^^^^^^^^^^^^

In update operation, route is defined uniquely for the corresponding tuple's player_id::

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
^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^

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

Teams Table
-----------

This table consists of 4 columns::

| Column Name   | Data Type | Key                   |
| ------------- |:---------:| ---------------------:|
| TEAM_ID       | serial    | PRIMARY KEY           |
| NAME          | varchar   | none                  |
| LEAGUE_ID     | date      | FK LEAGUES(LEAGUE_ID) |

*Table Initialization*
^^^^^^^^^^^^^^^^^^^^^^

Table is created by following sql code::

   CREATE TABLE IF NOT EXISTS TEAMS
                    (
                    TEAM_ID serial NOT NULL PRIMARY KEY,
                    NAME varchar(100) NOT NULL,
                    LEAGUE_ID int NOT NULL REFERENCES LEAGUES(LEAGUE_ID)
                    )

*Selection*
^^^^^^^^^^^

If "/teams" route is loaded by GET method, teams are going to be selected and will be printed to teams.html::

   @app.route('/teams', methods=['GET', 'POST'])
   def teams():
    if request.method == 'GET':
        return render_template('teams.html', teams = app.teams.select_teams())
    else:
        name = request.form['name']
        league_id = request.form['league_id']
        app.teams.add_team(name,league_id)
    return redirect(url_for('teams'))

Selection operation is done by the following function which is in teams.py::

   def select_teams(self):
         with dbapi2.connect(self.app.config['dsn']) as connection:
              cursor = connection.cursor()
              query = """ SELECT * FROM TEAMS ORDER BY TEAM_ID """
              cursor.execute(query)
              connection.commit()

              teams = cursor.fetchall()
              return teams

*Insert Operation*
^^^^^^^^^^^^^^^^^^

A route is defined in order to use Team Adding html page Leagues are selected and added to Dropdown Menu since League_id is foreign key.::

   @app.route('/teams/add', methods=['GET', 'POST'])
   def add_teams():
    return render_template('teams_add.html', leagues = app.leagues.get_leagues())

After the form is filled and submitted in page, form action directs to the following route::

   @app.route('/teams', methods=['GET', 'POST'])
   def teams():
    if request.method == 'GET':
        return render_template('teams.html', teams = app.teams.select_teams())
    else:
        name = request.form['name']
        league_id = request.form['league_id']
        app.teams.add_team(name,league_id)
    return redirect(url_for('teams'))

If "/teams" route is loaded by POST method, which is the team addition form's method, team will be added and route will redirect to itself again.
If route is loaded by GET method, teams.html page will be opened up.

Insertion operation is done by the following function which is in teams.py::

   def add_team(self, name, league_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO TEAMS (NAME, LEAGUE_ID) VALUES (%s, %s) """
                cursor.execute(query, (name, league_id))
                connection.commit()

*Update Operation*
^^^^^^^^^^^^^^^^^^

In update operation, route is defined uniquely for the corresponding tuple's team_id.::

   @app.route('/teams/update/<team_id>', methods=['GET', 'POST'])
   def update_teams(team_id):
    if request.method == 'GET':
        return render_template('teams_edit.html', team = app.teams.get_team(team_id), leagues = app.leagues.get_leagues())
    else:
        name = request.form['name']
        league_id = request.form['league_id']
        app.teams.update_team(team_id, name, league_id)
        return redirect(url_for('teams'))

If the route is loaded by GET method, team with corresponding team_id will be selected to update and route will be directed to teams_edit.html::

   def get_team(self, team_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM TEAMS WHERE TEAM_ID = %s """
             cursor.execute(query, [team_id])
             connection.commit()
             team = cursor.fetchall()
             return team

The form's action in teams_edit.html redirects form to the current route. Since form's method is POST, route is loaded by POST method.
Values are requested from form and the update function is called. After that, route redirects to teams page.
Update operation is done by the following function in teams.py::

   def update_team(self, team_id, name, league_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ UPDATE TEAMS
                        SET NAME = %s,
                        LEAGUE_ID = %s
                        WHERE
                        TEAM_ID = %s """
                cursor.execute(query, (name, league_id, team_id))
                connection.commit()


*Delete Operation*
^^^^^^^^^^^^^^^^^^

Delete operation is very similar to Update operation. Like update, in delete operation, route is defined uniquely for the corresponding tuple's team id.::

   @app.route('/teams/delete/<team_id>', methods=['GET', 'POST'])
   def delete_teams(team_id):
    app.teams.delete_team(team_id)
    return redirect(url_for('teams'))

After the team is deleted, route redirects to players page. Delete operation is done by the following function in teams.py::

    def delete_team(self, team_id):
         with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """ DELETE FROM TEAMS WHERE TEAM_ID = %s """
            cursor.execute(query, [team_id])
            connection.commit()

*Search Operation*
^^^^^^^^^^^^^^^^^^

A route is defined in order to search teams by team name. Search form is in teams.html::

   @app.route('/teams/search', methods = ['GET', 'POST'])
   def search_teams():
    if request.method == 'GET':
        return redirect(url_for('teams_search.html'))
    else:
        searchname = request.form['nametosearch']
        return render_template('teams_search.html', teams = app.teams.search_team(searchname))


Since the form has POST method, after the submission, search name will be requested from form. After searching, results will be listed in teams_search.html.

Searching is done by the following function in teams.py::

   def search_team(self, name):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ SELECT * FROM TEAMS WHERE NAME LIKE %s ORDER BY TEAM_ID """
                cursor.execute(query, ['%'+name+'%'])
                teams = cursor.fetchall()
                return teams

Squads Table
------------

This table consists of 4 columns::

| Column Name   | Data Type | Key                   |
| ------------- |:---------:| ---------------------:|
| SQUAD_ID      | serial    | PRIMARY KEY           |
| TEAM_ID       | int       | FK TEAMS(TEAM_ID)     |
| PLAYER_ID     | int       | FK PLAYERS(PLAYER_ID) |
| KIT_NO        | int       | none                  |

*Table Initialization*
^^^^^^^^^^^^^^^^^^^^^^

Table is created by following sql code::

   CREATE TABLE IF NOT EXISTS SQUADS
                    (
                    SQUAD_ID serial NOT NULL PRIMARY KEY,
                    TEAM_ID int NOT NULL REFERENCES TEAMS(TEAM_ID),
                    PLAYER_ID int NOT NULL UNIQUE REFERENCES PLAYERS(PLAYER_ID),
                    KIT_NO int NOT NULL
                    )
*Selection*
^^^^^^^^^^^

If "/squads" route is loaded by GET method, squads are going to be selected and will be printed to squads.html::

   @app.route('/squads', methods=['GET', 'POST'])
   def squads():
    if request.method == 'GET':
        return render_template('squads.html', teams = app.squads.get_teams(), squads = app.squads.show_squads())
    else:
        team_id = request.form['team_id']
        player_id = request.form['player_id']
        kit_no = request.form['kit_no']
        app.squads.add_squad(team_id, player_id, kit_no)
    return redirect(url_for('squads'))

Selection is made in a way that, instead of using team_id and player_id, team name and player name corresponding to their id's are selected using LEFT JOIN.
Selection operation is done by the following function which is in squads.py::

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

*Insert Operation*
^^^^^^^^^^^^^^^^^^

A route is defined in order to use Squad Adding html page. Teams and Players are selected and added to Dropdown Menus since they're foreign keys.::

   @app.route('/squads/add', methods=['GET', 'POST'])
   def add_squads():
    return render_template('squads_add.html', teams = app.teams.select_teams(), players = app.squads.get_players())


After the form is filled and submitted in page, form action directs to the following route::

   @app.route('/squads', methods=['GET', 'POST'])
   def squads():
    if request.method == 'GET':
        return render_template('squads.html', teams = app.squads.get_teams(), squads = app.squads.show_squads())
    else:
        team_id = request.form['team_id']
        player_id = request.form['player_id']
        kit_no = request.form['kit_no']
        app.squads.add_squad(team_id, player_id, kit_no)
    return redirect(url_for('squads'))


If "/squads" route is loaded by POST method, which is the squad addition form's method, team will be added and route will redirect to itself again.
If route is loaded by GET method, squads.html page will be opened up.

Insertion operation is done by the following function which is in squads.py::

   def add_squad(self, team_id, player_id, kit_no):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """ INSERT INTO SQUADS (TEAM_ID, PLAYER_ID, KIT_NO) VALUES (%s, %s, %s) """
                cursor.execute(query, (team_id, player_id, kit_no))
                connection.commit()

*Update Operation*
^^^^^^^^^^^^^^^^^^

In update operation, route is defined uniquely for the corresponding tuple's squad_id.::

   @app.route('/squads/update/<squad_id>', methods=['GET', 'POST'])
   def update_squads(squad_id):
       if request.method == 'GET':
           return render_template('squads_edit.html', squad = app.squads.get_squad(squad_id), teams = app.teams.select_teams(), players = app.players.select_players())
       else:
           team_id = request.form['team_id']
           player_id = request.form['player_id']
           kit_no = request.form['kit_no']
           app.squads.update_squad(squad_id, team_id, player_id, kit_no)
           return redirect(url_for('squads'))

If the route is loaded by GET method, team with corresponding squad_id will be selected to update and route will be directed to squads_edit.html::

   def get_squad(self, squad_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM SQUADS WHERE SQUAD_ID = %s """
             cursor.execute(query, [squad_id])
             connection.commit()
             squad = cursor.fetchall()
             return squad

The form's action in squads_edit.html redirects form to the current route. Since form's method is POST, route is loaded by POST method.
Values are requested from form and the update function is called. After that, route redirects to squads page.
Update operation is done by the following function in squads.py::

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


*Delete Operation*
^^^^^^^^^^^^^^^^^^

Delete operation is very similar to Update operation. Like update, in delete operation, route is defined uniquely for the corresponding tuple's squad id.::

   @app.route('/squads/delete/<squad_id>', methods=['GET', 'POST'])
   def delete_squads(squad_id):
       app.squads.delete_squad(squad_id)
       return redirect(url_for('squads'))

After the team is deleted, route redirects to squads page. Delete operation is done by the following function in squads.py::

    def delete_squad(self, squad_id):
         with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """ DELETE FROM SQUADS WHERE SQUAD_ID = %s """
            cursor.execute(query, [squad_id])
            connection.commit()

*Search Operation*
^^^^^^^^^^^^^^^^^^

A route is defined in order to search and filter squads by team name. Searching is made in a way that in squads.html, team names are selected and added to a dropdown list.
And squads can be filtered by selecting team name. Search form is in squads.html::

   @app.route('/squads/search', methods = ['GET', 'POST'])
   def search_squads():
    if request.method == 'GET':
        return redirect(url_for('squads_search.html'), teams = app.squads.get_teams())
    else:
        team_id = request.form['name']
        return render_template('squads_search.html', teams = app.squads.get_teams(), squads = app.squads.search_squad(team_id))

Team names ae selected by the following function in squads.py. This function selects team names distinctly. To obtain team name corresponding to team_id, LEFT JOIN is used.::

   def get_teams(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT DISTINCT teams.team_id, teams.name FROM SQUADS
                     LEFT JOIN TEAMS
                     ON SQUADS.TEAM_ID = TEAMS.TEAM_ID ORDER BY TEAM_ID"""
             cursor.execute(query)
             connection.commit()
             teams = cursor.fetchall()
             return teams


Since the form has POST method, after the submission, search name will be requested from form. After searching, results will be listed in squads_search.html.

Searching is done by the following function in squads.py::

   def search_squad(self, team_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query =  """ SELECT squad_id, teams.name, players.name, kit_no FROM SQUADS
                     LEFT JOIN TEAMS
                     ON SQUADS.TEAM_ID = TEAMS.TEAM_ID
                     LEFT JOIN PLAYERS
                     ON SQUADS.PLAYER_ID = PLAYERS.PLAYER_ID
                     WHERE SQUADS.TEAM_ID = %s
                     ORDER BY SQUADS.TEAM_ID """
             cursor.execute(query, [team_id])
             connection.commit()
             squad = cursor.fetchall()
             return squad

