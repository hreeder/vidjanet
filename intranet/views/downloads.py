from intranet import app
from intranet.models.downloads import DownloadFile, DownloadTag

from flask import render_template

@app.route("/downloads")
@app.route("/downloads/tagged/<tagname>")
def downloads_index(tagname=None):
	tags = DownloadTag.query.order_by(DownloadTag.name).all()
	if tagname:
		tag = DownloadTag.query.filter_by(name=tagname).first_or_404()
		downloads = tag.files.all()
	else:
		downloads = DownloadFile.query.all()
	return render_template("downloads.html", downloads=downloads, tags=tags)
