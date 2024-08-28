from extensions import db


class Team(db.Model):
    __tablename__ = 'team'
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(20), nullable=False)
    stadion_name = db.Column(db.String(100))


class Player(db.Model):
    __tablename__ = 'player'
    player_id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(20))
    nationality = db.Column(db.String(30))


class Coach(db.Model):
    __tablename__ = 'coach'
    coach_id = db.Column(db.Integer, primary_key=True)
    coach_name = db.Column(db.String(20))


class Position(db.Model):
    __tablename__ = 'position'
    position_id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(20))


class TeamPlayer(db.Model):
    __tablename__ = 'team_player'
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'), primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.position_id'), nullable=False)


class TeamCoach(db.Model):
    __tablename__ = 'team_coach'
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.coach_id'), primary_key=True)
