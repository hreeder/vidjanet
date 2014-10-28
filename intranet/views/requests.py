from intranet import app, db
from intranet.filters import get_possible_days
from intranet.models.timeslots import Timeslot
from intranet.models.games import Game, GameVote
from intranet.models.music import TrackRequest

from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_required, current_user

from werkzeug import secure_filename

import os

@app.route('/schedule')
def view_schedule():
	possible_days = get_possible_days()
	days = []

	for day in possible_days:
		slots = Timeslot.query.filter_by(day=day['code']).all()
		day['slots'] = slots
		days.append(day)

	primary = Game.query.filter_by(primary=True).all()
	othergames =  Game.query.filter_by(primary=False).all()
	
	return render_template('schedule.html', possible_days=days, primary=primary, othergames=othergames)

@app.route("/schedule/vote/<slotid>/<gameid>")
@login_required
def vote_for_game(slotid, gameid):
	slot = Timeslot.query.filter_by(id=slotid).first()
	if not slot:
		flash("Invalid Time Slot", "danger")

	game = Game.query.filter_by(id=gameid).first()
	if not game:
		flash("Invalid Game ID", "danger")

	if slot and game:
		userid = current_user.id

		# Let's see if the user has already voted on this poll
		existing_vote = GameVote.query.filter_by(slot_id=slotid, user_id=userid).first()

		if existing_vote:
			flash("You cannot vote more than once on a poll", "danger")
		else:
			# Ok, they didn't already vote, let's create the vote
			vote = GameVote(slot_id=slotid, user_id=userid, game_id=gameid)

			db.session.add(vote)
			db.session.commit()
		
	return redirect("/schedule")


@app.route("/music", methods=['GET', 'POST'])
def view_song_requests():
	if request.method == "POST":
		# If the visitor has somehow been logged out before posting this form
		# We should make them re-log
		if current_user.is_anonymous():
			flash("You must be logged in to do that", "danger")
			return redirect("/login")

		# We've added a new request, let's create and store it
		title = request.form['songtitle']
		artist = request.form['artist']

		# If we have a file upload then we should store it somewhere
		file = request.files['songupload']
		filename = ""
		if file and "." in file.filename and file.filename.rsplit(".", 1)[1] in app.config['MUSIC_ALLOWED_EXTENSIONS']:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['MUSIC_UPLOAD_FOLDER'], filename))

		songrequest = TrackRequest(title=title, artist=artist, user_id=current_user.get_id(), url=filename, played=False)
		db.session.add(songrequest)
		db.session.commit()

	requests = TrackRequest.query.filter_by(played=False).all()
	played = TrackRequest.query.filter_by(played=True).order_by("id desc").limit(5).all()

	return render_template("music.html", requests=requests, played=played)
