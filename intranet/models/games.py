from intranet import db

class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	primary = db.Column(db.Boolean)

class GameVote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	slot_id = db.Column(db.Integer, db.ForeignKey('timeslot.id'))
	game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
	user_id = db.Column(db.Integer)