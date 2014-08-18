from intranet import app
from intranet.classes.users import admin

from flask import render_template

@app.route("/admin")
@admin
def admin_index():
	return render_template("admin/index.html")