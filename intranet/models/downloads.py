from intranet import db

downloads_tagged = db.Table('downloads_tagged',
	db.Column('download_id', db.Integer(), db.ForeignKey('download_file.id')),
	db.Column('tag_id', db.Integer(), db.ForeignKey('download_tag.id')))

class DownloadTag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))

class DownloadFile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	url = db.Column(db.String(128))
