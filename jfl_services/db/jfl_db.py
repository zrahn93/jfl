import argparse
import random

import mysql.connector
from datetime import date

class Database:
    def __init__(self, host, user, password, database):
        self._db = self._connect(host=host, user=user, password=password, database=database)

    def _connect(self, host, user, password, database):
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def create_db(self):
        cursor = self._db.cursor()

        cursor.execute("CREATE TABLE users ( \
            user_id INT AUTO_INCREMENT PRIMARY KEY, \
            name VARCHAR(255), \
            active BOOL \
        );")
        cursor.execute("CREATE TABLE weeks ( \
            week_id INT AUTO_INCREMENT PRIMARY KEY, \
            number INT, \
            year INT, \
            complete BOOL \
        );")
        cursor.execute("CREATE TABLE teams ( \
            team_id INT AUTO_INCREMENT PRIMARY KEY, \
            name VARCHAR(255), \
            year INT, \
            bye_week INT, \
            FOREIGN KEY(bye_week) REFERENCES weeks(week_id)\
        );")
        cursor.execute("CREATE TABLE games (\
            game_id INT PRIMARY KEY AUTO_INCREMENT, \
            week_id INT, \
            FOREIGN KEY(week_id) REFERENCES weeks(week_id), \
            home_team_id INT, \
            FOREIGN KEY(home_team_id) REFERENCES teams(team_id), \
            away_team_id INT, \
            FOREIGN KEY(away_team_id) REFERENCES teams(team_id), \
            home_odds INT, \
            away_odds INT, \
            home_score INT, \
            away_score INT, \
            winning_team_id INT, \
            FOREIGN KEY(winning_team_id) REFERENCES teams(team_id), \
            losing_team_id INT, \
            FOREIGN KEY(losing_team_id) REFERENCES teams(team_id), \
            tie BOOL \
        );")
        cursor.execute("CREATE TABLE user_selections (\
            selection_id INT PRIMARY KEY AUTO_INCREMENT, \
            user_id INT, \
            FOREIGN KEY(user_id) REFERENCES users(user_id), \
            week_id INT, \
            FOREIGN KEY(week_id) REFERENCES weeks(week_id), \
            team_id INT, \
            FOREIGN KEY(team_id) REFERENCES teams(team_id), \
            draft_order INT, \
            result VARCHAR(255) \
        );")

    def create_season(self, users, weeks, nfl_teams, schedule):
        year = date.today().year

        cursor = self._db.cursor()
        cursor.execute("SELECT name, active FROM users")
        all_users = cursor.fetchall()

        # Add users that don't exist
        NAME, ACTIVE = (0, 1)
        for user_name in users:
            if user_name not in [u[NAME] for u in all_users]:
                cursor.execute('INSERT INTO users (name, active) VALUES (%s, %s)', (user_name, True))
            elif user_name not in [u[NAME] for u in all_users if u[ACTIVE]]:
                cursor.execute("UPDATE users SET active = true WHERE name = %s", user_name)
        self._db.commit()

        # Add weeks
        vals = [(week, year, False) for week in weeks]
        cursor.executemany("INSERT INTO weeks (number, year, complete) VALUES (%s, %s, %s);", vals)
        self._db.commit()

        #cursor.execute("SELECT * FROM weeks WHERE year = '%s';", year)
        WEEK_NUMBER_INDEX = 1
        cursor.execute("SELECT * FROM weeks WHERE year=%s;", (year,))
        all_weeks = cursor.fetchall()
        all_weeks = {w[WEEK_NUMBER_INDEX]: w for w in all_weeks}

        # Add teams
        WEEK_ID_INDEX = 0
        vals = [(team['name'], year, all_weeks[team['bye_week']][WEEK_ID_INDEX]) for team in nfl_teams]
        cursor.executemany("INSERT INTO teams (name, year, bye_week) VALUES (%s, %s, %s);", vals)
        self._db.commit()

        TEAM_ID, TEAM_NAME = (0, 1)
        cursor.execute("SELECT * FROM teams WHERE year=%s;", (year,))
        all_teams = cursor.fetchall()
        all_teams = {t[TEAM_NAME]: t for t in all_teams}

        # Add schedule
        query = "INSERT INTO games (week_id, home_team_id, away_team_id) VALUES ("
        vals = []
        for week_number, week_matchups in schedule.items():
            for matchup in week_matchups:
                vals.append((
                    all_weeks[week_number][WEEK_ID_INDEX],
                    all_teams[matchup['home_team']][TEAM_ID],
                    all_teams[matchup['away_team']][TEAM_ID]
                ))

        cursor.executemany("INSERT INTO games (week_id, home_team_id, away_team_id) VALUES (%s, %s, %s);", vals)
        self._db.commit()

    def set_draft_order(self, week, year, order):
        cursor = self._db.cursor(buffered=True)
        cursor.execute("SELECT week_id FROM weeks WHERE number = %s and year = %s;", (week, year))
        week_id = cursor.fetchone()[0]

        vals = []
        for order_i, name in enumerate(order):
            draft_pick = order_i + 1

            cursor.execute("SELECT user_id FROM users WHERE name = %s;", (name, ))
            user_id = cursor.fetchone()[0]

            vals.append((week_id, user_id, draft_pick))

        cursor.executemany("INSERT INTO user_selections (week_id, user_id, draft_order) VALUES (%s, %s, %s);", vals)
        self._db.commit()

    def create_drafts(self, bye_weeks, year=date.today().year):
        #TODO: For now, bye weeks will be entered manually. Eventually figure out Tom Shea's logic.
        cursor = self._db.cursor()
        cursor.execute("SELECT name FROM users WHERE active = true")
        all_teams = [x[0] for x in cursor.fetchall()]

        for week, bye_teams in bye_weeks.items():
            cursor.execute("SELECT COUNT(*) from teams where bye_week != %s and year = %s", (week, year))
            nfl_teams_this_week = cursor.fetchone()[0]

            teams_playing = [t for t in all_teams if t not in bye_teams]
            random.shuffle(teams_playing)

            # Construct snake draft
            full_draft = []
            for _ in range((nfl_teams_this_week // len(teams_playing)) // 2):
                two_rounds = teams_playing + list(reversed(teams_playing))
                full_draft = full_draft + two_rounds

            # Add to the database
            self.set_draft_order(week, year, full_draft)

    def add_user(self, name):
        cursor = self._db.cursor()
        cursor.execute("INSERT INTO users (name, active) VALUES (%s, true);", (name,))
        db.commit()

    def deactivate_user(self, name):
        cursor = self._db.cursor()
        cursor.execute("UPDATE users SET active false WHERE name = %s;", (name,))
        db.commit()

    def get_current_week(self, year):
        cursor = self._db.cursor()
        cursor.execute("SELECT MIN(number) FROM weeks WHERE year = %s AND complete IS FALSE;", (year,))
        result = cursor.fetchone()[0]

        return result

    def get_teams_playing(self, week, year):
        cursor = self._db.cursor()
        cursor.execute(" \
            SELECT home_team_id, home_team.name,  home_odds, away_team_id, away_team.name, away_odds, \
                   home_score, away_score \
            FROM games \
                LEFT JOIN teams home_team ON home_team.team_id=games.home_team_id \
                LEFT JOIN teams away_team ON away_team.team_id=games.away_team_id \
            WHERE games.week_id = (SELECT week_id FROM weeks WHERE number = %s AND year = %s);", (week, year))
        matchups = cursor.fetchall()

        team_ids = set()
        for matchup in matchups:
            team_ids.add(str(matchup[0]))
            team_ids.add(str(matchup[3]))
        team_ids = ','.join(team_ids)

        cursor.execute("SELECT home_team_id, away_team_id, winning_team_id, losing_team_id, tie \
            FROM games WHERE home_team_id IN (%s) OR away_team_id IN (%s);" % (team_ids, team_ids)
        )
        season_games = cursor.fetchall()

        teams = []
        for matchup in matchups:
            home_games = [g for g in season_games if str(matchup[0]) == str(g[0])] #home wins
            away_games = [g for g in season_games if str(matchup[0]) == str(g[1])] #away wins
            wins = (
                len([g for g in home_games if str(matchup[0]) == str(g[2])]) + 
                len([g for g in away_games if str(matchup[0]) == str(g[2])])
            )
            losses = (
                len([g for g in home_games if str(matchup[0]) == str(g[3])]) + 
                len([g for g in away_games if str(matchup[0]) == str(g[3])])
            )
            ties = (
                len([g for g in home_games if g[4] == 1]) + 
                len([g for g in away_games if g[4] == 1])
            )
            teams.append({
                'team_id': matchup[0],
                'team': matchup[1],
                'odds': matchup[2],
                'opponent': matchup[4],
                'wins': wins,
                'losses': losses,
                'ties': ties,
                'home': True,
                'finished': matchup[6] is not None and matchup[7] is not None
            })

            #Away team
            home_games = [g for g in season_games if str(matchup[3]) == str(g[0])] #home wins
            away_games = [g for g in season_games if str(matchup[3]) == str(g[1])] #away wins
            wins = (
                len([g for g in home_games if str(matchup[3]) == str(g[2])]) + 
                len([g for g in away_games if str(matchup[3]) == str(g[2])])
            )
            losses = (
                len([g for g in home_games if str(matchup[3]) == str(g[3])]) + 
                len([g for g in away_games if str(matchup[3]) == str(g[3])])
            )
            ties = (
                len([g for g in home_games if g[4] == 1]) + 
                len([g for g in away_games if g[4] == 1])
            )
            teams.append({
                'team_id': matchup[3],
                'team': matchup[4],
                'odds': matchup[5],
                'opponent': matchup[1],
                'wins': wins,
                'losses': losses,
                'ties': ties,
                'home': False,
                'finished': matchup[6] is not None and matchup[7] is not None
            })

        return teams

    def update_odds(self, week, home_team, away_team, home_odds, away_odds, year=date.today().year):
        cursor = self._db.cursor()
        cursor.execute("UPDATE games \
            SET home_odds = %s, away_odds = %s \
            WHERE ( \
                week_id = (SELECT week_id FROM weeks WHERE number = %s AND year = %s)[0] AND \
                home_team_id IN (SELECT team_id FROM teams WHERE name = '%s') AND \
                away_team_id IN (SELECT team_id FROM teams WHERE name = '%s') \
            );",
            (home_odds, away_odds, week, year, home_team, away_team)
        )
        self._db.commit()

    def select_team(self, user_id, week, pick, team, year=date.today().year):
        cursor = self._db.cursor()
        cursor.execute("UPDATE user_selections SET team_id = ( \
                (SELECT team_id FROM teams where name = %s and year = %s) \
            ) WHERE \
                user_id = %s AND \
                draft_order = %s AND \
                week_id IN (SELECT week_id FROM weeks WHERE number = %s AND year = %s)",
            (team, year, user_id, pick, week, year)
        )
        self._db.commit()

    def get_current_picks(self, week, year):
        cursor = self._db.cursor()
        cursor.execute("SELECT user_selections.draft_order, users.user_id, users.name, teams.team_id, teams.name \
            FROM user_selections \
                LEFT JOIN users ON users.user_id=user_selections.user_id \
                LEFT JOIN teams ON teams.team_id=user_selections.team_id \
                LEFT JOIN weeks ON weeks.week_id=user_selections.week_id \
            WHERE weeks.week_id IN ( \
                SELECT week_id FROM weeks WHERE number = %s AND year = %s \
            ) ORDER BY user_selections.draft_order;" % (week, year)
        )
        results = cursor.fetchall()

        return results

    def reset_picks(self, week, year):
        cursor = self._db.cursor()

        cursor.execute("UPDATE games \
                LEFT JOIN weeks ON weeks.week_id=games.week_id \
            SET games.winning_team_id = NULL, losing_team_id = NULL, home_score = NULL, away_score = NULL, tie = NULL \
            WHERE weeks.number = %s AND weeks.year = %s;",
            (week, year)
        )
        self._db.commit()

        cursor.execute("UPDATE user_selections \
                LEFT JOIN weeks ON weeks.week_id=user_selections.week_id \
            SET user_selections.team_id = NULL \
            WHERE weeks.number = %s AND weeks.year = %s;",
            (week, year)
        )
        self._db.commit()

    def sim_week(self, week, year):
        cursor = self._db.cursor()
        cursor.execute("SELECT game_id, home_team.name,  away_team.name \
            FROM games \
                LEFT JOIN weeks ON weeks.week_id=games.week_id \
                LEFT JOIN teams home_team ON home_team.team_id=games.home_team_id \
                LEFT JOIN teams away_team ON away_team.team_id=games.away_team_id \
            WHERE weeks.number = %s AND weeks.year = %s;",
            (week, year)
        )
        results = cursor.fetchall()

        for game_info in results:
            home_score = random.randint(17, 31)
            away_score = random.randint(14, 30)
            self.update_score(week, game_info[1], game_info[2], home_score, away_score, year)

    def update_score(self, week, home_team, away_team, home_score, away_score, year=date.today().year):
        cursor = self._db.cursor()
        cursor.execute("SELECT team_id, name \
            FROM teams \
            WHERE name IN (%s, %s) AND year = %s;",
            (home_team, away_team, year)
        )
        results = cursor.fetchall()
        home_team_id = [team for team in results if team[1] == home_team][0][0]
        away_team_id = [team for team in results if team[1] == away_team][0][0]

        tie = False
        if home_score > away_score:
            winning_team_id = home_team_id
            losing_team_id = away_team_id
        elif home_score < away_score:
            winning_team_id = away_team_id
            losing_team_id = home_team_id
        else:
            tie = True
            prefix = "SET tie = 1"

        if not tie:
            prefix = "SET winning_team_id = %s, losing_team_id = %s, tie = 0" % (winning_team_id, losing_team_id)

        prefix += ", home_score = %d, away_score = %d" % (home_score, away_score)

        query = f"UPDATE games \
            {prefix} \
            WHERE ( \
                week_id = (SELECT week_id FROM weeks WHERE number = %s AND year = %s) AND \
                home_team_id = %s AND \
                away_team_id = %s \
            );"

        cursor.execute(query, (week, year, home_team_id, away_team_id))
        self._db.commit()

    def complete_week(self, number, year):
        cursor = self._db.cursor()
        cursor.execute("UPDATE weeks \
            SET complete = 1 \
            WHERE (number = %s AND year = %s);",
            (number, year)
        )
        self._db.commit()

    def get_season_selections(self, year):
        cursor = self._db.cursor()
        cursor.execute("SELECT week_id, number FROM weeks WHERE year = %s;", (year,))
        weeks = cursor.fetchall()

        results = {}
        for week in weeks:
            weekly_selections = self.get_current_picks(week[1], year)
            results[week[0]] = { "week": week[1], "users": {} }
            # user_selections.draft_order, users.user_id, users.name, teams.team_id, teams.name
            users = {x[2] for x in weekly_selections}
            for user in users:
                user_selections = [x for x in weekly_selections if x[2] == user]
                results[week[0]]["users"][user] = user_selections

        return results

    def get_standings(self, year):
        cursor = self._db.cursor()
        cursor.execute("SELECT user_id, name FROM users;")
        users = cursor.fetchall()

        standings = []
        for user in users:
            user_info = self.get_user_info(user[0], year)
            del user_info['draft_selections']
            user_info["user_id"] = user[0]

            total_games = user_info['wins'] + user_info['losses'] + user_info['ties']
            if total_games == 0:
                user_info['win_pct'] = 0.0
            else:
                user_info['win_pct'] = (
                    (2 * user_info['wins'] + user_info['ties']) / 
                    (2 * (user_info['wins'] + user_info['losses'] + user_info['ties']))
                )

            standings.append(user_info)

        standings = sorted(standings, key=lambda x: x['win_pct'], reverse=True)
        return standings

    def get_team_info(self, team_id):
        cursor = self._db.cursor()
        cursor.execute("SELECT name FROM teams WHERE team_id = %s;", (team_id,))
        team_name = cursor.fetchall()[0][0]

        cursor.execute("SELECT winning_team_id, losing_team_id, tie \
            FROM games WHERE home_team_id = %s OR away_team_id = %s;",
            (team_id, team_id)
        )
        results = cursor.fetchall()

        wins = len([game for game in results if str(game[0]) == str(team_id)])
        losses = len([game for game in results if str(game[1]) == str(team_id)])
        ties = len([game for game in results if game[2] == 1])

        results = (team_name, wins, losses, ties)

        # Get NLF schedule with scores

        return results

    def get_user_info(self, user_id, year=date.today().year):
        cursor = self._db.cursor()
        # Get all of the user's selections
        cursor.execute("SELECT weeks.number, users.user_id, users.name, teams.team_id, teams.name, weeks.week_id \
            FROM user_selections \
                LEFT JOIN users ON users.user_id=user_selections.user_id \
                LEFT JOIN teams ON teams.team_id=user_selections.team_id \
                LEFT JOIN weeks ON weeks.week_id=user_selections.week_id \
            WHERE users.user_id = %s AND weeks.year = %s;", (user_id, year)
        )
        selections = cursor.fetchall()

        # Get wins/losses of those selections
        picks = [{"team_id": info[3], "week": info[5], 'info': info} for info in selections if info[3] is not None]
        team_ids = {str(info[3]) for info in selections if info[3] is not None}

        results = []
        if len(team_ids) > 0:
            team_ids = ','.join(team_ids)
            cursor.execute("SELECT week_id, home_team_id, away_team_id, winning_team_id, losing_team_id, tie \
                FROM games \
                WHERE home_team_id IN (%s) OR away_team_id IN (%s);" % (team_ids, team_ids)
            )
            results = cursor.fetchall()

        wins = 0
        losses = 0
        ties = 0

        pick_results = []
        for pick in picks:
            for result in results:
                if pick["week"] == result[0] and pick["team_id"] in [result[1], result[2]]:
                    pick["info"] = list(pick["info"])
                    if pick["team_id"] == result[3]:
                        wins += 1
                        pick["info"].append('win')
                    elif pick["team_id"] == result[4]:
                        losses += 1
                        pick["info"].append('loss')
                    elif result[5] == 1:
                        ties += 1
                        pick["info"].append('tie')
                    break

        user_name = None
        weekly_results = []

        if len(picks) > 0:
            user_name = picks[0]["info"][2]
            weeks = set([x["info"][0] for x in picks])

            for week in weeks:
                games = [game["info"] for game in picks if game["info"][0] == week]
                # Checking if all the selections are the same (only true when all None)
                if games.count(games[0][3]) != len(games):
                    weekly_results.append(games)

        #sort weekly_results by descending week number
        weekly_results = sorted(weekly_results, key=lambda x: x[0], reverse=True)

        if user_name is None:
            cursor.execute("SELECT name FROM users WHERE user_id = %s;", (user_id,))
            user_results = cursor.fetchone()
            if user_results is not None:
                user_name = user_results[0]

        return {
            "user_name": user_name,
            "draft_selections": weekly_results,
            "wins": wins,
            "losses": losses,
            "ties": ties
        }


if __name__ == '__main__':
    db = Database(
        host="localhost",
        user="jeff",
        password="password",
        database="jfl"
    )

    try:
        db.create_db()
    except mysql.connector.errors.ProgrammingError as e:
        print(e)
        print("Database already exists")

    parser = argparse.ArgumentParser()
    parser.add_argument("--populate", action='store_true', help="Populate with a simulated year")
    args = parser.parse_args()

    if args.populate:
        # Define users
        users = [
            "Zac Rahn",
            "Jeremy Rahn",
            "Jon Weiner",
            "Tom Shea",
            "Chris Stanziale",
            "Nicky Stanziale",
            "Pichael Stanziale",
            "Eugene Rapay",
            "Dillon Kelly",
            "Jack Goldman",
            "Nick Cabrese"
        ]
        weeks = [w + 1 for w in range(18)]

        # Get the NFL teams
        nfl_teams = [
            {'name': 'Arizona Cardinals', 'bye_week': 4},
            {'name': 'Atlanta Falcons', 'bye_week': 4},
            {'name': 'Baltimore Ravens', 'bye_week': 5},
            {'name': 'Buffalo Bills', 'bye_week': 5},
            {'name': 'Carolina Panthers', 'bye_week': 6},
            {'name': 'Chicago Bears', 'bye_week': 6},
            {'name': 'Cincinnati Bengals', 'bye_week': 7},
            {'name': 'Cleveland Browns', 'bye_week': 7},
            {'name': 'Dallas Cowboys', 'bye_week': 8},
            {'name': 'Denver Broncos', 'bye_week': 8},
            {'name': 'Detroit Lions', 'bye_week': 9},
            {'name': 'Green Bay Packers', 'bye_week': 9},
            {'name': 'Houston Texans', 'bye_week': 10},
            {'name': 'Indianapolis Colts', 'bye_week': 10},
            {'name': 'Jacksonville Jaguars', 'bye_week': 11},
            {'name': 'Kansas City Chiefs', 'bye_week': 11},
            {'name': 'Las Vegas Raiders', 'bye_week': 12},
            {'name': 'Los Angeles Chargers', 'bye_week': 12},
            {'name': 'Los Angeles Rams', 'bye_week': 13},
            {'name': 'Miami Dolphins', 'bye_week': 13},
            {'name': 'Minnesota Vikings', 'bye_week': 14},
            {'name': 'New England Patriots', 'bye_week': 14},
            {'name': 'New Orleans Saints', 'bye_week': 15},
            {'name': 'New York Giants', 'bye_week': 15},
            {'name': 'New York Jets', 'bye_week': 16},
            {'name': 'Philadelphia Eagles', 'bye_week': 16},
            {'name': 'Pittsburgh Steelers', 'bye_week': 17},
            {'name': 'San Francisco 49ers', 'bye_week': 17},
            {'name': 'Seattle Seahawks', 'bye_week': 18},
            {'name': 'Tampa Bay Buccaneers', 'bye_week': 18},
            {'name': 'Tennessee Titans', 'bye_week': 3},
            {'name': 'Washington Commanders', 'bye_week': 3},
        ]

        # Get the NFL schedule/matchups
        schedule = {}
        for w in weeks:
            teams_playing = [team['name'] for team in nfl_teams if w != team['bye_week']]
            random.shuffle(teams_playing)
            schedule[w] = []
            for i in range(len(teams_playing) // 2):
                schedule[w].append({
                    "home_team": teams_playing[i*2],
                    "away_team": teams_playing[i*2 + 1],
                })

        # Add this information to the database
        db.create_season(users, weeks, nfl_teams, schedule)

        # Create draft orders for each week
        bye_weeks = {}
        for w in weeks:
            random.shuffle(users)
            bye_weeks[w] = [users[i] for i in range(random.randint(0, 3))]

        db.create_drafts(bye_weeks)
