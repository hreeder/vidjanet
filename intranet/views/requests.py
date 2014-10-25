from intranet import app
from intranet.filters import get_possible_days
from intranet.models.timeslots import Timeslot
from intranet.models.games import Game
from flask import render_template

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