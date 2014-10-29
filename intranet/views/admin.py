from intranet import app, db, r
from intranet.classes.users import admin
from intranet.filters import get_possible_days
from intranet.models.downloads import DownloadTag, DownloadFile
from intranet.models.timeslots import Timeslot
from intranet.models.games import Game
from intranet.models.music import TrackRequest

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

		musicuri = request.form['musicuri']
		downloadsuri = request.form['downloadsuri']

		r.set(app.config['SETTING_PREFIX'] + "music-base-url", musicuri)
		r.set(app.config['SETTING_PREFIX'] + "downloads-base-url", downloadsuri)

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

@app.route("/admin/schedule/poll/<slotid>")
@admin
def view_poll(slotid):
	games = Game.query.all()
	slot = Timeslot.query.filter_by(id=slotid).first()

	if not slot:
		flash("Timeslot not found", "danger")
		return redirect("/admin/schedule")

	return render_template("admin/poll.html", slot=slot, games=games)

@app.route("/admin/music")
@admin
def view_song_requests_dj():
	upcoming = TrackRequest.query.filter_by(played=False).all()
	played = TrackRequest.query.filter_by(played=True).all()

	return render_template("admin/music.html", upcoming=upcoming, played=played)

@app.route("/admin/music/play/<songid>")
@admin
def mark_song_played(songid):
	track = TrackRequest.query.filter_by(id=songid).first_or_404()

	track.played = True
	db.session.add(track)
	db.session.commit()

	return redirect("/admin/music")

@app.route("/admin/downloads", methods=["GET", "POST"])
@admin
def admin_downloads():
	if request.method == "POST":
		# We've posted the new download form.
		# Process it
		title = request.form['title']
		description = request.form['description']
		tags = request.form['tags']
		file = request.files['file']
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['DOWNLOAD_UPLOAD_FOLDER'], filename))

		dlfile = DownloadFile(title=title, description=description, url=filename)

		# We may have some tags too
		if tags:
			if "," in tags:
				tags = tags.split(",")

				# Remove leading/trailing whitespace from tags
				tags = [tag.trim() for tag in tags]
			else:
				# Remove leading/trailing whitespace
				tags = tags.trim()

				# We're going to make tags a list just so we don't get individual letter tags
				tags = [tags,]

			for tag in tags:
				newtag = DownloadTag(name=tag)
				db.session.add(newtag)

		# TODO: Add tags to actual downloadable file

	downloads = DownloadFile.query.all()
	return render_template("admin/downloads.html", downloads=downloads)
