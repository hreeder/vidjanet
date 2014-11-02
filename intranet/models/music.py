from intranet import db, users

class TrackRequest(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128))
	artist = db.Column(db.String(128))
	url = db.Column(db.String(128))
	user_id = db.Column(db.Integer)
	played = db.Column(db.Boolean)
	votes = db.Column(db.Integer)

	def get_requester(self):
		return users.get_user(user_id=self.user_id)
