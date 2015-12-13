import psycopg2 as dbapi2
import datetime
import json
import os
import re

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask.helpers import url_for

from coaches import Coaches, Coaches2
from coaching import Coaching,Coaching2
from countries import Countries, Country
from leagues import Leagues, League
from matches import Matches, Match
from teams import Team, Teams
from stadiums import Stadium, Stadiums
from officials import Officials, Official
from players import Player, Players
from seasons import Seasons, Seasons2
from statisticsTeam import StatisticT, StatisticsT
from statisticsPlayer import StatisticP, StatisticsP
from fixtures import Fixture, Fixtures
from squads import Squad, Squads
from transfers import Transfer, Transfers
from flask.templating import render_template_string


app = Flask(__name__)

'''ElephantSQL configurations'''
def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

'''Home Page'''
@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


'''Coaches Pages'''
@app.route('/coaches', methods=['GET', 'POST'])
def coaches():
    if request.method == 'GET':
        return render_template('coaches.html', result = app.coaches.select_coaches())
    else:
        if 'Add' in request.form:
            name = request.form['coachName']
            birthday = request.form['coachBirthday']
            app.coaches.add_coach(name, birthday)
            return redirect(url_for('coaches'))
        elif 'Delete' in request.form:
            id = request.form['id']
            app.coaches.delete_coach(id)
            return redirect(url_for('coaches'))
        elif 'Update' in request.form:
            id = request.form['id']
            name = request.form['coachNUpdate']
            birthday = request.form['coachBUpdate']
            app.coaches.update_coach(id,name,birthday )
            return redirect(url_for('coaches'))
        elif 'Search' in request.form:
            name = request.form['coachSearch']
            return render_template('coaches.html', result = app.coaches.search_coach(name))
        else:
            return render_template('coaches.html', result = app.coaches.select_coaches())

'''Coaching Pages'''
@app.route('/coaching', methods=['GET', 'POST'])
def coaching():
    if request.method == 'GET':
        return render_template('coaching.html', coachlist=app.coaching.get_coaching(), teams = app.teams.choose_teams_coaching(), season=app.seasons.select_seasons(),coaches=app.coaches.select_coaches() ,coaching = app.coaching.select_coaching())
    else:
        if 'Add' in request.form:
            team_id = request.form['team_id']
            coach_id = request.form['coach_id']
            season_id = request.form['season_id']
            app.coaching.add_coaching(team_id,coach_id,season_id)
            return redirect(url_for('coaching'))
        elif 'Delete' in request.form:
            coaching_id = request.form['id']
            app.coaching.delete_coaching(coaching_id)
            return redirect(url_for('coaching'))
        elif 'Update' in request.form:
            coaching_id = request.form['id']
            team_id = request.form['team_idU']
            coach_id = request.form['coach_idU']
            season_id = request.form['season_idU']
            app.coaching.update_coaching(coaching_id,team_id,coach_id,season_id)
            return redirect(url_for('coaching'))
        elif 'Search' in request.form:
            term = request.form['coachingSearch']
            return render_template('coaching.html', coachlist = app.coaching.search_coaching(term))
        else:
            return render_template('coaching.html', result = app.coaching.select_coaching())


'''Countries Pages'''
@app.route('/countries', methods=['GET', 'POST'])
def countries():
    if request.method == 'GET':
        return render_template('countries.html', countries = app.countries.get_countries())
    else:
        if 'Add' in request.form:
            name = request.form['name']
            abbreviation = request.form['abbreviation']
            app.countries.add_country(Country(name, abbreviation))
            return render_template('countries.html', countries = app.countries.get_countries())
        elif 'Delete' in request.form:
            id = request.form['id']
            app.countries.delete_country(id)
            return render_template('countries.html', countries = app.countries.get_countries())
        elif 'Search' in request.form:
            search_terms = request.form['search_terms']
            return render_template('countries.html', countries = app.countries.search_countries(search_terms))


@app.route('/countries/add')
def countries_add():
     return render_template('country_add.html')

@app.route('/countries/edit/<country_id>', methods=['GET', 'POST'])
def country_edit(country_id):
    if request.method == 'GET':
        return render_template('country_edit.html', key = country_id, country=app.countries.get_country(country_id))
    else:
        name = request.form['name']
        abbreviation = request.form['abbreviation']
        app.countries.update_country(country_id, Country(name, abbreviation))
        return render_template('countries.html', countries = app.countries.get_countries())

'''*******************************************************************************************************'''

'''Fixtures Pages'''
@app.route('/fixtures', methods = ['GET', 'POST'])
def fixtures():
    if request.method == 'GET':
        return render_template('fixtures.html', result = app.fixtures.get_fixtures())
    else:
        season = request.form['season_id']
        team = request.form['team_id']
        points = request.form['points']
        app.fixtures.add_fixture(season, team, points)
    return render_template('fixtures.html', result = app.fixtures.get_fixtures())


@app.route('/fixtures/edit', methods = ['GET', 'POST'])
def add_fixture():
    if request.method == 'GET':
        return render_template('fixture_add.html', team=app.teams.select_teams(), season=app.seasons.select_seasons(), result = app.fixtures.get_fixtures())
    else:
        season = request.form['season_id']
        team = request.form['team_id']
        points = request.form['points']
        app.fixtures.add_fixture(season, team, points)
    return redirect(url_for('add_fixture'))

@app.route('/fixtures/delete', methods = ['GET', 'POST'])
def delete_fixture():
    if request.method == 'GET':
        return render_template('fixtures.html', result = app.fixtures.get_fixtures())
    else:
        id = request.form['id']
        app.fixtures.delete_fixture(id)
    return redirect(url_for('add_fixture'))

@app.route('/fixtures/update', methods = ['GET', 'POST'])
def update_fixture():
    if request.method == 'GET':
        return render_template('fixture_update.html', team=app.teams.select_teams(), season=app.seasons.select_seasons(), result = app.fixtures.get_fixtures())
    else:
        fixture_id = request.form['fixture_id']
        season = request.form['season_id']
        team = request.form['team_id']
        points = request.form['points']
        app.fixtures.update_fixture(fixture_id, season, team, points)
    return redirect(url_for('update_fixture'))

@app.route('/fixtures/search', methods=['GET', 'POST'])
def search_fixture():
    if request.method == 'GET':
        return render_template('fixture_search.html')
    else:
        id = request.form['id']
        return render_template('fixture_search.html',result=app.fixtures.search_fixture(id))


'''*******************************************************************************************************'''

'''Matches Pages'''
@app.route('/matches', methods=['GET', 'POST'])
def matches():
    if request.method == 'GET':
        return render_template('matches.html', matches = app.matches.get_matches())
    else:
        if request.form['submit']=="Save":
            season_id = request.form['seasonID']
            home_id = request.form['homeID']
            away_id = request.form['awayID']
            official_id = request.form['officialID']
            result = request.form['result']
            match=Match(season_id,official_id,home_id,away_id,result)
            app.matches.add_match(match)
        else:
            id = request.form['id']
            season_id = request.form['seasonID']
            home_id = request.form['homeID']
            away_id = request.form['awayID']
            official_id = request.form['officialID']
            result = request.form['result']
            match=Match(season_id,official_id,home_id,away_id,result)
            app.matches.update_match(id,match)

        return redirect(url_for('matches'))

@app.route('/matches/', methods=['GET', 'POST'])
def match_determine():
    if request.method=='GET':
        return redirect(url_for('matches'))
    if request.form['id']=="0":
        return redirect(url_for('matches'))
    if request.form['submit'] == "Delete":
        id = request.form['id']
        form = request.form
        form_data={id: form['id']}
        return redirect(url_for('match_delete'), code=307 )
    elif request.form['submit'] == "Update":
        return render_template('match_update.html', id = request.form['id'], teams=app.teams.select_teams(),
                             season=app.seasons.select_seasons(),officials=app.officials.get_officials() )
    else:
        return redirect(url_for('matches'))

@app.route('/matches/add', methods=['GET', 'POST'])
def match_add():
     return render_template('matches_edit.html', teams=app.teams.select_teams(),
                             season=app.seasons.select_seasons(),officials=app.officials.get_officials())

@app.route('/matches/delete', methods=['GET', 'POST'])
def match_delete():
    if request.method == 'GET':
        return render_template_string("""You need to click delete button at the end of the desired match.
                                            Return to the list of matches.
                                            <form action="{{ url_for('match') }}" method="get" role="form">
                                            <div class="form-group">
                                            <input value="Return" name="Return" type="submit" /><br><br>
                                            </div> <!-- End of form-group -->
                                            </form>""")
    else:
        id = request.form['id']
        app.matches.delete_match(id)
        return redirect(url_for('matches'))

@app.route('/matches/update', methods=['GET', 'POST'])
def match_update():
    if request.method == 'GET':
        return render_template('matches.html', matches = app.matches.get_matches())
    else:
        return render_template('match_update.html', id = request.form['id'])

'''Officials Pages'''
@app.route('/officials', methods=['GET', 'POST'])
def officials():
    if request.method == 'GET':
        return render_template('officials.html', officials = app.officials.get_officials())
    else:
        if request.form['submit']=="Save":
            name = request.form['name']
            age = request.form['age']
            app.officials.add_official(name, age)
        else:
            id = request.form['id']
            name = request.form['name']
            age = request.form['age']
            official = Official(name,age)
            app.officials.update_official(id, official)

        return redirect(url_for('officials'))

@app.route('/officials/add', methods=['GET', 'POST'])
def official_add():
     return render_template('official_edit.html')

@app.route('/officials/', methods=['GET', 'POST'])
def official_determine():
    if request.form['submit'] == "Search":
        return redirect(url_for('search_official'))
    elif request.form['submit'] == "Delete":
        id = request.form['id']
        form = request.form
        form_data={id: form['id']}
        return redirect(url_for('official_delete'), code=307 )
    elif request.form['submit'] == "Update":
        id = request.form['id']
        form = request.form
        form_data={id: form['id']}
        return redirect(url_for('update_official'), code=307 )
    else:
        return redirect(url_for('officials'))

@app.route('/officials/delete', methods=['GET', 'POST'])
def official_delete():
    if request.method == 'GET':
        return render_template_string("""You need to click delete button at the end of the desired official.
                                            Return to the list of officials.
                                            <form action="{{ url_for('officials') }}" method="get" role="form">
                                            <div class="form-group">
                                            <input value="Return" name="Return" type="submit" /><br><br>
                                            </div> <!-- End of form-group -->
                                            </form>""")
    else:
        id = request.form['id']
        app.officials.delete_official(id)
        return redirect(url_for('officials'))

@app.route('/officials/search', methods=['GET', 'POST'])
def search_official():
    if request.method == 'GET':
        return render_template('official_search.html')
    else:
        name = request.form['name']
        id = request.form['id']
        return render_template('official_search.html',result=app.officials.search_officials(name, id))

@app.route('/officials/update', methods=['GET', 'POST'])
def update_official():
    if request.method == 'GET':
        return render_template('officials.html', officials = app.officials.get_officials())
    else:
        return render_template('official_update.html', id = request.form['id'])

'''Leagues Pages'''
@app.route('/leagues', methods=['GET', 'POST'])
def leagues():
    if request.method == 'GET':
        return render_template('leagues.html', leagues = app.leagues.get_leagues())
    else:
        if 'Add' in request.form:
            name = request.form['name']
            abbreviation =request.form['abbreviation']
            country_id = request.form['countryID']
            app.leagues.add_league(League(name, abbreviation, country_id))
            return redirect(url_for('leagues'))
        elif 'Delete' in request.form:
            id = request.form['id']
            app.leagues.delete_league(id)
            return render_template('leagues.html', leagues = app.leagues.get_leagues())
        elif 'Search' in request.form:
            search_terms = request.form['search_terms']
            return render_template('leagues.html', leagues = app.leagues.search_leagues(search_terms))

@app.route('/leagues/add')
def leagues_edit():
    return render_template('league_edit.html', countries = app.countries.get_countries())

'''Player Pages'''
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

@app.route('/players/search', methods = ['GET', 'POST'])
def search_players():
    if request.method == 'GET':
        return redirect(url_for('players_search.html'))
    else:
        searchname = request.form['nametosearch']
        return render_template('players_search.html', players = app.players.search_player(searchname))

@app.route('/players/add', methods=['GET', 'POST'])
def add_players():
    return render_template('players_add.html')

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

@app.route('/players/delete/<player_id>', methods=['GET', 'POST'])
def delete_players(player_id):
    app.players.delete_player(player_id)
    return redirect(url_for('players'))


'''Seasons Pages'''

@app.route('/seasons', methods=['GET', 'POST'])
def seasons():
    if request.method == 'GET':
           return render_template('seasons.html', result = app.seasons.select_seasons())
    else:
        if 'Add' in request.form:
            year = request.form['seasonYear']
            app.seasons.add_season(year)
            return redirect(url_for('seasons'))
        elif 'Delete' in request.form:
            id = request.form['id']
            app.seasons.delete_season(id)
            return redirect(url_for('seasons'))
        elif 'Update' in request.form:
            id = request.form['id']
            year = request.form['seasonUpdate']
            app.seasons.update_season(id,year)
            return redirect(url_for('seasons'))
        elif 'Search' in request.form:
            year = request.form['seasonSearch']
            return render_template('seasons.html', result = app.seasons.search_season(year))
        else:
            return render_template('seasons.html', result = app.seasons.select_seasons())


'''Stadiums Pages'''
@app.route('/stadiums', methods=['GET', 'POST'])
def stadiums():
    if request.method == 'GET':
        return render_template('stadiums.html', stadiums = app.stadiums.get_stadiums())
    else:
        if 'Add' in request.form:
            name = request.form['name']
            capacity = request.form['capacity']
            country_id = request.form['country_id']
            team_id = request.form['team_id']
            app.stadiums.add_stadium(name, capacity, country_id, team_id)
            return render_template('stadiums.html', stadiums = app.stadiums.get_stadiums())
        elif 'Delete' in request.form:
            stadium_id = request.form['stadium_id']
            app.stadiums.delete_stadium(stadium_id)
            return render_template('stadiums.html', stadiums = app.stadiums.get_stadiums())
        elif 'Search' in request.form:
            search_terms = request.form['search_terms']
            return render_template('stadiums.html', stadiums = app.stadiums.search_stadiums(search_terms))

@app.route('/stadiums/add')
def stadiums_add():
    return render_template('stadium_add.html' , countries = app.countries.get_countries(), teams = app.teams.select_teams())

@app.route('/stadiums/edit/<stadium_id>', methods=['GET', 'POST'])
def stadiums_edit(stadium_id):
    if request.method == 'GET':
        return render_template('stadium_edit.html', key = country_id, country=app.countries.get_country(country_id))
    else:
        name = request.form['name']
        abbreviation = request.form['abbreviation']
        app.countries.update_country(country_id, Country(name, abbreviation))
        return render_template('countries.html', countries = app.countries.get_countries())

''' Squad Pages '''
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

@app.route('/squads/add', methods=['GET', 'POST'])
def add_squads():
    return render_template('squads_add.html', teams = app.teams.select_teams(), players = app.squads.get_players())

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

@app.route('/squads/delete/<squad_id>', methods=['GET', 'POST'])
def delete_squads(squad_id):
    app.squads.delete_squad(squad_id)
    return redirect(url_for('squads'))

@app.route('/squads/search', methods = ['GET', 'POST'])
def search_squads():
    if request.method == 'GET':
        return redirect(url_for('squads_search.html'), teams = app.squads.get_teams())
    else:
        team_id = request.form['name']
        return render_template('squads_search.html', teams = app.squads.get_teams(), squads = app.squads.search_squad(team_id))

'''Statistics Pages'''
@app.route('/statistics/teams', methods = ['GET', 'POST'])
def statistics_team():
    if request.method == 'GET':
        return render_template('statistics_team.html', result = app.statisticsTeam.get_statistics_team())
    else:
        season = request.form['season_id']
        team = request.form['team_id']
        touchdowns = request.form['touchdowns']
        rushingYards = request.form['rushingYards']
        app.statisticsTeam.add_statistic_team(season, team, touchdowns, rushingYards)
    return render_template('statistics_team.html', result = app.statisticsTeam.get_statistics_team())

@app.route('/statistics/players', methods = ['GET', 'POST'])
def statistics_player():
    if request.method == 'GET':
        return render_template('statistics_player.html', result = app.statisticsPlayer.get_statistics_player())
    else:
        season = request.form['season_id']
        player = request.form['player_id']
        tackles = request.form['tackles']
        penalties = request.form['penalties']
        app.statisticsPlayer.add_statistic_player(season, player, tackles, penalties)
    return render_template('statistics_player.html', result = app.statisticsPlayer.get_statistics_player())


'''Team Statistics Pages'''
@app.route('/statistics/teams/add', methods = ['GET', 'POST'])
def add_statistic_team():
    if request.method == 'GET':
        return render_template('statistic_team_add.html', team=app.teams.select_teams(), season=app.seasons.select_seasons(), result = app.statisticsTeam.get_statistics_team())
    else:
        season = request.form['season_id']
        team = request.form['team_id']
        touchdowns = request.form['touchdowns']
        rushingYards = request.form['rushingYards']
        app.statisticsTeam.add_statistic_team(season, team, touchdowns, rushingYards)
    return redirect(url_for('add_statistic_team'))

@app.route('/statistics/teams/delete', methods = ['GET', 'POST'])
def delete_statistic_team():
    if request.method == 'GET':
        return render_template('statistics_team.html', result = app.statisticsTeam.get_statistics_team())
    else:
        id = request.form['id']
        app.statisticsTeam.delete_statistic_team(id)
    return redirect(url_for('add_statistic_team'))

@app.route('/statistics/teams/update', methods = ['GET', 'POST'])
def update_statistic_team():
    if request.method == 'GET':
        return render_template('statistic_team_update.html', team=app.teams.select_teams(), season=app.seasons.select_seasons(), result = app.statisticsTeam.get_statistics_team())
    else:
        statistic_id = request.form['statistic_id']
        season = request.form['season_id']
        team = request.form['team_id']
        touchdowns = request.form['touchdowns']
        rushingYards = request.form['rushingYards']
        app.statisticsTeam.update_statistic_team(statistic_id, season, team, touchdowns, rushingYards)
    return redirect(url_for('update_statistic_team'))

@app.route('/statistics/teams/search', methods=['GET', 'POST'])
def search_statistic_team():
    if request.method == 'GET':
        return render_template('statistic_team_search.html')
    else:
        id = request.form['id']
        return render_template('statistic_team_search.html',result=app.statisticsTeam.search_statistic_team(id))



    '''Players Statistics Pages'''

@app.route('/statistics/players/add', methods = ['GET', 'POST'])
def add_statistic_player():
    if request.method == 'GET':
        return render_template('statistic_player_add.html', player=app.players.select_players(), season=app.seasons.select_seasons(), result = app.statisticsPlayer.get_statistics_player())
    else:
        season = request.form['season_id']
        player = request.form['player_id']
        tackles = request.form['tackles']
        penalties = request.form['penalties']
        app.statisticsPlayer.add_statistic_player(season, player, tackles, penalties)
    return redirect(url_for('add_statistic_player'))

@app.route('/statistics/players/delete', methods = ['GET', 'POST'])
def delete_statistic_player():
    if request.method == 'GET':
        return render_template('statistics_player.html', result = app.statisticsPlayer.get_statistics_player())
    else:
        id = request.form['id']
        app.statisticsPlayer.delete_statistic_player(id)
    return redirect(url_for('add_statistic_player'))

@app.route('/statistics/players/update', methods = ['GET', 'POST'])
def update_statistic_player():
    if request.method == 'GET':
        return render_template('statistic_player_update.html', player=app.players.select_players(), season=app.seasons.select_seasons(), result = app.statisticsPlayer.get_statistics_player())
    else:
        statistic_id = request.form['statistic_id']
        season = request.form['season_id']
        player = request.form['player_id']
        tackles = request.form['tackles']
        penalties = request.form['penalties']
        app.statisticsPlayer.update_statistic_player(statistic_id, season, player, tackles, penalties)
    return redirect(url_for('update_statistic_player'))

@app.route('/statistics/players/search', methods=['GET', 'POST'])
def search_statistic_player():
    if request.method == 'GET':
        return render_template('statistic_player_search.html')
    else:
        id = request.form['id']
        return render_template('statistic_player_search.html',result=app.statisticsPlayer.search_statistic_player(id))


'''Team pages'''
@app.route('/teams', methods=['GET', 'POST'])
def teams():
    if request.method == 'GET':
        return render_template('teams.html', teams = app.teams.select_teams())
    else:
        name = request.form['name']
        league_id = request.form['league_id']
        app.teams.add_team(name,league_id)
    return redirect(url_for('teams'))

@app.route('/teams/search', methods = ['GET', 'POST'])
def search_teams():
    if request.method == 'GET':
        return redirect(url_for('teams_search.html'))
    else:
        searchname = request.form['nametosearch']
        return render_template('teams_search.html', teams = app.teams.search_team(searchname))

@app.route('/teams/add', methods=['GET', 'POST'])
def add_teams():
    return render_template('teams_add.html', leagues = app.leagues.get_leagues())

@app.route('/teams/update/<team_id>', methods=['GET', 'POST'])
def update_teams(team_id):
    if request.method == 'GET':
        return render_template('teams_edit.html', team = app.teams.get_team(team_id), leagues = app.leagues.get_leagues())
    else:
        name = request.form['name']
        league_id = request.form['league_id']
        app.teams.update_team(team_id, name, league_id)
        return redirect(url_for('teams'))

@app.route('/teams/delete/<team_id>', methods=['GET', 'POST'])
def delete_teams(team_id):
    app.teams.delete_team(team_id)
    return redirect(url_for('teams'))



@app.route('/transfers', methods=['GET', 'POST'])
def transfers():
    if request.method == 'GET':
        return render_template('transfers.html', transfers = app.transfers.get_transfers())
    else:
        if request.form['submit']=="Save":
            season_id = request.form['seasonID']
            old_id = request.form['oldID']
            new_id = request.form['newID']
            player_id = request.form['playerID']
            fee = request.form['fee']
            transfer=Transfer(season_id,player_id,old_id,new_id,fee)
            app.transfers.add_transfer(transfer)
        else:
            id = request.form['id']
            season_id = request.form['seasonID']
            old_id = request.form['oldID']
            new_id = request.form['newID']
            player_id = request.form['playerID']
            fee = request.form['fee']
            transfer=Transfer(season_id,player_id,old_id,new_id,fee)
            app.transfers.update_transfer(id, transfer)

        return redirect(url_for('transfers'))

@app.route('/transfers/', methods=['GET', 'POST'])
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

@app.route('/transfers/add', methods=['GET', 'POST'])
def transfer_add():
     return render_template('transfer_edit.html', teams=app.teams.select_teams(),
                             season=app.seasons.select_seasons(),players=app.players.select_players())

@app.route('/transfers/delete', methods=['GET', 'POST'])
def transfer_delete():
    if request.method == 'GET':
        return render_template_string("""You need to click delete button at the end of the desired match.
                                            Return to the list of matches.
                                            <form action="{{ url_for('transfer') }}" method="get" role="form">
                                            <div class="form-group">
                                            <input value="Return" name="Return" type="submit" /><br><br>
                                            </div> <!-- End of form-group -->
                                            </form>""")
    else:
        id = request.form['id']
        app.transfers.delete_transfer(id)
        return redirect(url_for('transfers'))

@app.route('/transfer/update', methods=['GET', 'POST'])
def transfer_update():
    if request.method == 'GET':
        return render_template('transfers.html', transfers = app.transfers.get_transfers())
    else:
        return render_template('transfer_update.html', id = request.form['id'])


'''Database initialization'''
@app.route('/initdb')
def create_tables():

    '''Reference order in DB should be preserved'''
    app.coaches.initialize_tables()
    app.seasons.initialize_tables()
    app.countries.initialize_tables()
    app.players.initialize_tables()
    app.leagues.initialize_tables()
    app.teams.initialize_tables()
    app.stadiums.initialize_tables()
    app.coaching.initialize_tables()
    app.squads.initialize_tables()

    app.officials.initialize_tables()
    app.matches.initialize_tables()
    app.transfers.initialize_tables()

    app.statisticsTeam.initialize_tables()
    app.statisticsPlayer.initialize_tables()
    app.fixtures.initialize_tables()

    return redirect(url_for('home_page'))


'''Database Drop All tables'''
@app.route('/drop')
def drop_tables():
    with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
                rows = cursor.fetchall()
                for row in rows:
                    cursor.execute("drop table " + row[1] + " cascade")

                connection.commit()
    return redirect(url_for('create_tables'))

if __name__ == '__main__':

    '''Container objects'''

    app.coaches = Coaches2(app)
    app.coaching = Coaching2(app)
    app.teams = Teams(app)
    app.players = Players(app)
    app.countries = Countries(app)
    app.leagues = Leagues(app)
    app.stadiums = Stadiums(app)
    app.officials = Officials(app)
    app.seasons = Seasons2(app)
    app.matches = Matches(app)
    app.statisticsTeam = StatisticsT(app)
    app.statisticsPlayer = StatisticsP(app)
    app.fixtures = Fixtures(app)
    app.squads = Squads(app)
    app.transfers = Transfers(app)

    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
          app.config['dsn'] = """user='vagrant' password='vagrant'
                            host='localhost' port=54321 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)
