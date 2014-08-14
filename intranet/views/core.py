from intranet import app

@app.route("/")
@app.route("/<name>")
def index(name=None):
	if name:
		return "Hello, %s"  % (name,)
	return "Hello, World"