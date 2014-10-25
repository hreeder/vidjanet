from intranet import db

class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	primary = db.Column(db.Boolean)