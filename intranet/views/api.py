from intranet import app, r
from flask import jsonify

@app.route("/api/v1/rvb.json")
def rvb_json():
	prefix = app.config['SETTING_PREFIX'] + "RvB"
	enabled = r.get(prefix)
	if enabled == "False":
		return jsonify(status="disabled")

	red = r.get(prefix+"-red-score")
	blue = r.get(prefix+"-blue-score")

	return jsonify(status="enabled", red_score=red, blue_score=blue)