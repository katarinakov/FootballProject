from flask import Blueprint, request, jsonify
from extensions import db
from models import Team, Player, Coach, TeamPlayer, Position, TeamCoach

bp = Blueprint('teams', __name__, url_prefix='/teams')


# Getting all Teams
@bp.route('/', methods=['GET'])
def get_teams():
    # Get all Teams
    teams = Team.query.all()

    result = []

    for team in teams:
        # Get Players in the Team
        team_players = TeamPlayer.query.filter_by(team_id=team.team_id).all()
        player_names = [Player.query.get(tp.player_id).player_name for tp in team_players]

        # Get Coaches in the Team
        team_coaches = TeamCoach.query.filter_by(team_id=team.team_id).all()
        coach_names = [Coach.query.get(tc.coach_id).coach_name for tc in team_coaches]

        result.append({
            'teamId': team.team_id,
            'teamName': team.team_name,
            'stadionName': team.stadion_name,
            'players': player_names,
            'coaches': coach_names
        })

    return jsonify(result)


# Making of a new Team
@bp.route('/', methods=['POST'])
def create_team():
    data = request.json
    new_team = Team(team_name=data['teamName'], stadion_name=data.get('stadionName'))
    db.session.add(new_team)
    db.session.commit()
    return jsonify({'message': 'Team created successfully'}), 201


# Getting the Players and their Positions in a Team
@bp.route('/<int:team_id>/players', methods=['GET'])
def get_team_players(team_id):

    team_players = db.session.query(TeamPlayer, Player.player_name, Position.position_name).join(Player, Player.player_id == TeamPlayer.player_id).join(Position, Position.position_id == TeamPlayer.position_id).filter(TeamPlayer.team_id == team_id).all()

    players = [{'playerId': tp.TeamPlayer.player_id, 'playerName': tp.player_name, 'positionName': tp.position_name, 'teamId': tp.TeamPlayer.team_id, 'positionId': tp.TeamPlayer.position_id} for tp in team_players]

    return jsonify(players)


# Adding an existing Player to a Team and specifying the Position
@bp.route('/<int:team_id>/players', methods=['POST'])
def add_player_to_team(team_id):
    data = request.get_json()

    player_id = data.get('playerId')
    position_id = data.get('positionId')

    if not player_id or not position_id:
        return jsonify({'error': 'Missing playerId or positionId'}), 400

    # Check if the player exists
    player = Player.query.get(player_id)
    if not player:
        return jsonify({'error': 'Player not found'}), 404

    # Check if position exists
    position = Position.query.get(position_id)
    if not position:
        return jsonify({"error": "Position not found"}), 404

    team_player = TeamPlayer(team_id=team_id, player_id=player_id, position_id=position_id)
    db.session.add(team_player)
    db.session.commit()
    return jsonify({'message': 'Player added successfully to team!', 'playerId': player_id}), 201


# Adding an existing coach to the Team
@bp.route('/<int:team_id>/coaches', methods=['POST'])
def add_coach_to_team(team_id):
    data = request.json
    # Get information from json
    coach_id = data.get('coachId')

    if not coach_id:
        return jsonify({'error': 'Missing coachId'}), 400

    # Check if the coach exists
    coach = Coach.query.get(coach_id)
    if not coach:
        return jsonify({'error': 'Coach not found'}), 404

    team_coach = TeamCoach(team_id=team_id, coach_id=coach_id)
    db.session.add(team_coach)
    db.session.commit()
    return jsonify({'message': 'Coach added successfully to team!', 'playerId': coach_id}), 201


# Update information about a Player in a Team
@bp.route('/<int:team_id>/players/<int:player_id>', methods=['PUT'])
def update_player(team_id, player_id):
    data = request.json

    new_position_id = data.get('positionId')

    # Find if this Player is in this Team
    team_player = TeamPlayer.query.filter_by(team_id=team_id, player_id=player_id).first()
    if not team_player:
        return jsonify({'error': 'Player not found in this team'}), 404

    # Find if position exists
    position = Position.query.get(new_position_id)
    if not position:
        return jsonify({'error': 'Position not found'}), 404

    # Update the position of the player
    team_player.position_id = new_position_id

    db.session.commit()

    return jsonify({
        'message': 'Player position updated successfully',
        'teamId': team_id,
        'playerId': player_id
    })


# Delete the Team and all Players and Coaches with it
@bp.route('/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = Team.query.get(team_id)

    if not team:
        return jsonify({'error': 'Team not found'}), 404

    # Find all players and coaches that are associated with the team
    team_players = TeamPlayer.query.filter_by(team_id=team_id).all()
    team_coaches = TeamCoach.query.filter_by(team_id=team_id).all()

    # Delete all the players and coaches records
    for team_player in team_players:
        player = Player.query.get(team_player.player_id)
        if player:
            db.session.delete(player)  # Delete the player record

    for team_coach in team_coaches:
        coach = Coach.query.get(team_coach.coach_id)
        if coach:
            db.session.delete(coach)  # Delete the coach record

    db.session.query(TeamPlayer).filter_by(team_id=team_id).delete()
    db.session.query(TeamCoach).filter_by(team_id=team_id).delete()

    # Delete the Team
    db.session.delete(team)

    # Commit the changes to the database
    db.session.commit()

    # Return a success message
    return jsonify({
        'message': 'Team and all associated players and coaches deleted successfully'
    })


# Filter players in a Team by nationality
@bp.route('/<int:team_id>/filter', methods=['GET'])
def filter_players_by_nationality_in_team(team_id):
    nationality = request.args.get('nationality')

    if not nationality:
        return jsonify({'error': 'Nationality query parameter is required'}), 400

    # Step 1: Query the database to get the players in the specified team and filter by nationality
    players = db.session.query(Player).join(TeamPlayer).filter(
        TeamPlayer.team_id == team_id,
        Player.player_id == TeamPlayer.player_id,
        Player.nationality == nationality
    ).all()

    # Check if no players are found
    if not players:
        return jsonify({'message': 'No players found in this team with the specified nationality'}), 404

    players_data = [{
        'playerId': player.player_id,
        'playerName': player.player_name,
        'nationality': player.nationality
    } for player in players]

    return jsonify(players_data)




