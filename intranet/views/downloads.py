from intranet import app

@app.route("/downloads")
def downloads_index():
	return render_template("downloads.html")