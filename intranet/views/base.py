from intranet import app

@app.route("/")
def index():
	return "hello there"