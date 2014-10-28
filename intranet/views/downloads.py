from intranet import app

from flask import render_template

@app.route("/downloads")
def downloads_index():
	return render_template("downloads.html")
