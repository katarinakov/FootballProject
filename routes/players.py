from flask import Blueprint, request, jsonify
from models import Player, TeamPlayer
from extensions import db

bp = Blueprint('players', __name__, url_prefix='/players')


# Get all players in database
@bp.route('/', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([{'playerId': player.player_id, 'playerName': player.player_name, 'nationality': player.nationality} for player in players])


# Input a new player
@bp.route('/', methods=['POST'])
def create_player():
    data = request.json
    new_player = Player(player_name=data['playerName'], nationality=data['nationality'])
    db.session.add(new_player)
    db.session.commit()
    return jsonify({'message': 'Player created successfully'}), 201


# Update information about a Player
@bp.route('/<int:player_id>', methods=['PUT'])
def update_player(player_id):
    data = request.json
    player = Player.query.get(player_id)
    if player:
        player.player_name = data.get('playerName', player.player_name)
        player.nationality = data.get('nationality', player.nationality)
        db.session.commit()
        return jsonify({'message': 'Player updated successfully'})
    return jsonify({'message': 'Player not found'}), 404
