import os
import json
from datetime import date

from flask import Flask, g, jsonify, request, abort
from flask_cors import CORS #comment this on deployment

from db.jfl_db import Database

app = Flask(__name__)
CORS(app) #comment this on deployment


def get_db():
    '''
    Returns the document indexing object. Initializes a new Index object if one doesn't exist
    '''
    db = getattr(g, '_db', None)
    if db is None:
        db = Database(
            host="localhost",
            user="jeff",
            password="password",
            database="jfl"
        )
    return db


def validate_current_week_request(params):
    if params.get('year') is None:
        print("INFO: no 'year' attribute found in rewquest. Adding the current year")
        params['year'] = date.today().year


def generate_current_week_response(args):
    '''
    Returns a JSON response with the current week
    '''
    response = get_db().get_current_week(args['year'])
    return jsonify({"current_week": response})


def validate_teams_playing_request(params):
    errors = []
    if params.get('week') is None:
        print("ERROR: no 'week' attribute found in request.")
        errors.append("No 'week' attribute found in request.")
    if params.get('year') is None:
        print("INFO: no 'year' attribute found in rewquest. Adding the current year")
        params['year'] = date.today().year

    if len(errors) > 0:
        error_message = '\n' + '\n\t'.join(errors)
        abort(400, f"Invalid Request: {error_message}")


def generate_teams_playing_response(args):
    '''
    Returns a JSON response with the teams playing for the week
    '''
    response = get_db().get_teams_playing(args['week'], args['year'])
    return jsonify(response)


def validate_draft_status_request(params):
    errors = []
    if params.get('week') is None:
        print("ERROR: no 'week' attribute found in request.")
        errors.append("No 'week' attribute found in request.")
    if params.get('year') is None:
        print("INFO: no 'year' attribute found in rewquest. Adding the current year")
        params['year'] = date.today().year

    if len(errors) > 0:
        error_message = '\n' + '\n\t'.join(errors)
        abort(400, f"Invalid Request: {error_message}")


def generate_draft_status_response(args):
    '''
    Returns a JSON response with the teams playing for the week
    '''
    response = get_db().get_current_picks(args['week'], args['year'])
    return jsonify(response)


def validate_pick_team_request(params):
    errors = []
    if params.get('user_id') is None:
        print("ERROR: no 'user_id' attribute found in rewquest.")
        errors.append("No 'user_id' attribute found in request.")
    if params.get('week') is None:
        print("ERROR: no 'week' attribute found in request.")
        errors.append("No 'week' attribute found in request.")
    if params.get('pick') is None:
        print("ERROR: no 'pick' attribute found in request.")
        errors.append("No 'pick' attribute found in request.")
    if params.get('team') is None:
        print("ERROR: no 'team' attribute found in request.")
        errors.append("No 'team' attribute found in request.")
    if params.get('year') is None:
        print("INFO: no 'year' attribute found in request. Adding the current year")
        params['year'] = date.today().year

    if len(errors) > 0:
        error_message = '\n' + '\n\t'.join(errors)
        abort(400, f"Invalid Request: {error_message}")


def generate_pick_team_response(args):
    '''
    Runs the pick_teams db call
    Returns a JSON successful message upon completion
    '''
    get_db().select_team(args['user_id'], args['week'], args['pick'], args['team'], args['year'])
    return jsonify({"success": True})


def validate_season_picks_request(params):
    if params.get('year') is None:
        print("INFO: no 'year' attribute found in request. Adding the current year")
        params['year'] = date.today().year


def generate_season_picks_response(args):
    '''
    Returns a JSON response with the teams selected by week & user/player
    '''
    response = get_db().get_season_selections(args['year'])
    return jsonify(response)


def validate_standings_request(params):
    if params.get('year') is None:
        print("INFO: no 'year' attribute found in request. Adding the current year")
        params['year'] = date.today().year


def generate_standings_response(args):
    '''
    Returns a JSON response with NFL team information
    '''
    response = get_db().get_standings(args['year'])
    return jsonify(response)


def validate_team_data_request(params):
    if params.get('team_id') is None:
        print("ERROR: no 'team_id' attribute found in request.")
        abort(400, f"Invalid Request: no 'team_id' attribute found in request.")


def generate_team_data_response(args):
    '''
    Returns a JSON response with NFL team information
    '''
    response = get_db().get_team_info(args['team_id'])
    return jsonify(response)


def validate_user_data_request(params):
    if params.get('user_id') is None:
        print("ERROR: no 'user_id' attribute found in request.")
        abort(400, f"Invalid Request: no 'user_id' attribute found in request.")


def generate_user_data_response(args):
    '''
    Returns a JSON response with user information
    '''
    response = get_db().get_user_info(args['user_id'])
    return jsonify(response)


def validate_complete_week_request(params):
    errors = []
    if params.get('week') is None:
        print("ERROR: no 'week' attribute found in request.")
        abort(400, f"Invalid Request: no 'week' attribute found in request.")
    if params.get('year') is None:
        print("INFO: no 'year' attribute found in request. Adding the current year")
        params['year'] = date.today().year

    if len(errors) > 0:
        error_message = '\n' + '\n\t'.join(errors)
        abort(400, f"Invalid Request: {error_message}")


def generate_complete_week_response(args):
    '''
    Returns a JSON response verifying the week was completed
    '''
    response = get_db().complete_week(args['week'], args['year'])
    return jsonify({"success": True})


def validate_reset_week_request(params):
    errors = []
    if params.get('week') is None:
        print("ERROR: no 'week' attribute found in request.")
        abort(400, f"Invalid Request: no 'week' attribute found in request.")
    if params.get('year') is None:
        print("INFO: no 'year' attribute found in request. Adding the current year")
        params['year'] = date.today().year

    if len(errors) > 0:
        error_message = '\n' + '\n\t'.join(errors)
        abort(400, f"Invalid Request: {error_message}")


def generate_reset_week_response(args):
    '''
    Returns a JSON response verifying the draft picks were reset
    '''
    response = get_db().reset_picks(args['week'], args['year'])
    return jsonify({"success": True})


def validate_sim_games_request(params):
    errors = []
    if params.get('week') is None:
        print("ERROR: no 'week' attribute found in request.")
        abort(400, f"Invalid Request: no 'user_id' attribute found in request.")
    if params.get('year') is None:
        print("INFO: no 'year' attribute found in request. Adding the current year")
        params['year'] = date.today().year

    if len(errors) > 0:
        error_message = '\n' + '\n\t'.join(errors)
        abort(400, f"Invalid Request: {error_message}")


def generate_sim_games_response(args):
    '''
    Returns a JSON response verifying the games were simulated for the week
    '''
    response = get_db().sim_week(args['week'], args['year'])
    return jsonify({"success": True})


@app.route('/api/current_week', methods=['GET'])
def api_current_week():
    '''
    Route for the API to get the current week
    '''
    request_args = dict(request.args)
    validate_current_week_request(request_args)
    return generate_current_week_response(request_args)


@app.route('/api/teams_playing', methods=['GET'])
def api_get_teams_playing():
    '''
    Route for the API to get the teams playing
    '''
    request_args = dict(request.args)
    validate_teams_playing_request(request_args)
    return generate_teams_playing_response(request_args)


@app.route('/api/draft_status', methods=['GET'])
def api_draft_status():
    '''
    Route for the API to get the draft status
    '''
    request_args = dict(request.args)
    validate_draft_status_request(request_args)
    return generate_draft_status_response(request_args)


@app.route('/api/pick_team', methods=['POST'])
def api_pick_team():
    '''
    Route for the API to make a draft selection
    '''
    request_data = json.loads(request.data)
    validate_pick_team_request(request_data)
    return generate_pick_team_response(request_data)


@app.route('/api/season_selections', methods=['GET'])
def api_season_picks():
    '''
    Route for the API to get the league's picks for the entire season
    '''
    request_args = dict(request.args)
    validate_season_picks_request(request_args)
    return generate_season_picks_response(request_args)


@app.route('/api/standings', methods=['GET'])
def api_standings():
    '''
    Route for the API to get the standings of the league
    '''
    request_args = dict(request.args)
    validate_standings_request(request_args)
    return generate_standings_response(request_args)


@app.route('/api/team_data', methods=['GET'])
def api_team_data():
    '''
    Route for the API to get information about an NFL team
    '''
    request_args = dict(request.args)
    validate_team_data_request(request_args)
    return generate_team_data_response(request_args)


@app.route('/api/user_data', methods=['GET'])
def api_user_data():
    '''
    Route for the API to get information about a user
    '''
    request_args = dict(request.args)
    validate_user_data_request(request_args)
    return generate_user_data_response(request_args)


@app.route('/api/complete_week', methods=['POST'])
def api_complete_week():
    '''
    Route for the API to complete the week and move to the next week
    '''
    request_data = json.loads(request.data)
    validate_complete_week_request(request_data)
    return generate_complete_week_response(request_data)


@app.route('/api/reset_week', methods=['POST'])
def api_reset_week():
    '''
    Route for the API to reset the draft picks for a week
    '''
    request_data = json.loads(request.data)
    validate_reset_week_request(request_data)
    return generate_reset_week_response(request_data)


@app.route('/api/sim_games', methods=['POST'])
def api_sim_games():
    '''
    Route for the API to sim the games for a week
    '''
    request_data = json.loads(request.data)
    validate_sim_games_request(request_data)
    return generate_sim_games_response(request_data)


if __name__ == '__main__':
    # Run the app
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug)
