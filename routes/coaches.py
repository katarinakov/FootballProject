from flask import Blueprint, request, jsonify
from models import Coach, TeamCoach
from extensions import db

bp = Blueprint('coaches', __name__, url_prefix='/coaches')


# Get all Coaches
@bp.route('/', methods=['GET'])
def get_coaches():
    coaches = Coach.query.all()
    return jsonify([{'coachId': coach.coach_id, 'coachName': coach.coach_name} for coach in coaches])


@bp.route('/', methods=['POST'])
def create_coach():
    data = request.json
    new_coach = Coach(coach_name=data['coachName'])
    db.session.add(new_coach)
    db.session.commit()
    return jsonify({'message': 'Coach created successfully'}), 201


@bp.route('/<int:coach_id>', methods=['PUT'])
def update_coach(coach_id):
    data = request.json
    coach = Coach.query.get(coach_id)
    if coach:
        coach.coach_name = data.get('coachName', coach.coach_name)
        db.session.commit()
        return jsonify({'message': 'Coach updated successfully'})
    return jsonify({'message': 'Coach not found'}), 404
