from intranet import db

class Timeslot(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(32))
	start = db.Column(db.String(32))
	end = db.Column(db.String(32))
	votable = db.Column(db.Boolean)
	event = db.Column(db.String(128))

	def get_number_votes(self, gameid):
		return 0