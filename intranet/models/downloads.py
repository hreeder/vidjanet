from intranet import db

downloads_tagged = db.Table('downloads_tagged',
	db.Column('download_id', db.Integer(), db.ForeignKey('download_file.id')),
	db.Column('tag_id', db.Integer(), db.ForeignKey('download_tag.id')))

class DownloadTag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	files = db.relationship('DownloadFile', secondary=downloads_tagged,
		backref=db.backref('tags', lazy='dynamic'))

class DownloadFile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	description = db.Column(db.Text)
	url = db.Column(db.String(128))
	
	def get_tags(self):
		return [tag.name for tag in self.tags]
