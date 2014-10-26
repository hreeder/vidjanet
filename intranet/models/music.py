from intranet import db

class TrackRequest(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128))
	artist = db.Column(db.String(128))
	url = db.Column(db.String(128))
	user_id = db.Column(db.Integer)
	votes = db.Column(db.Integer)