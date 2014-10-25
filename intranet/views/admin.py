from intranet import app, db, r
from intranet.classes.users import admin
from intranet.filters import get_possible_days
from intranet.models.timeslots import Timeslot
from intranet.models.games import Game

from flask import redirect, render_template, request, flash

@app.route("/admin")
@admin
def admin_index():
	return render_template("admin/index.html")

@app.route("/admin/settings", methods=['GET', 'POST'])
@admin
def admin_settings():
	if request.method == "POST":
		eventno = request.form['eventno']
		startday = request.form['startday']
		endday = request.form['endday']

		r.set(app.config['SETTING_PREFIX'] + "eventno", eventno)
		r.set(app.config['SETTING_PREFIX'] + "startday", startday)
		r.set(app.config['SETTING_PREFIX'] + "endday", endday)

		flash("Settings Saved", "success")
	return render_template("admin/settings.html")

@app.route("/admin/settings/rvb")
@app.route("/admin/rvb/toggle")
@admin
def admin_toggle_rvb():
	curval = r.get(app.config['SETTING_PREFIX'] + "RvB")

	if curval == "False":
		r.set(app.config['SETTING_PREFIX'] + "RvB", "True")
	else:
		r.set(app.config['SETTING_PREFIX'] + "RvB", "False")

	if "toggle" in str(request.url_rule):
		return redirect("/admin/rvb")
	return redirect("/admin/settings")

@app.route("/admin/rvb")
@admin
def rvb_settings():
	return render_template('admin/rvb.html')

@app.route("/admin/schedule")
@admin
def event_schedule_settings():
	timeslots = Timeslot.query.all()
	possible_days = get_possible_days()
	games = Game.query.all()

	return render_template("admin/schedule.html", timeslots=timeslots, possible_days=possible_days, games=games)

@app.route("/admin/schedule/newslot", methods=['POST',])
@admin
def add_time_slot():
	day = request.form['day']
	start = request.form['start']
	end = request.form['end']

	if "votable" in request.form:
		votable = True
		event = ""
	else:
		votable = False
		event = request.form['event']

	newslot = Timeslot(day=day, start=start, end=end, votable=votable, event=event)

	db.session.add(newslot)
	db.session.commit()

	return redirect("/admin/schedule")

@app.route("/admin/schedule/delslot/<slotid>")
@admin
def del_time_slot(slotid):
	slot = Timeslot.query.filter_by(id=slotid).first()
	if slot:
		db.session.delete(slot)
		db.session.commit()
	else:
		flash("Timeslot not found", "danger")

	return redirect("/admin/schedule")

@app.route("/admin/schedule/newgame", methods=['POST',])
@admin
def add_game():
	name = request.form['gamename']
	if "primary" in request.form:
		primary = True
	else:
		primary = False

	newgame = Game(name=name, primary=primary)
	
	db.session.add(newgame)
	db.session.commit()

	return redirect("/admin/schedule")