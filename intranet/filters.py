from intranet import app, r

def get_day_info(current_code):
	if current_code == "mon":
		return {"day": "Monday", "code": "mon", "tomorrow": "tues"}
	elif current_code == "tues":
		return {"day": "Tuesday", "code": "tues", "tomorrow": "wed"}
	elif current_code == "wed":
		return {"day": "Wednesday", "code": "wed", "tomorrow": "thurs"}
	elif current_code == "thurs":
		return {"day": "Thursday", "code": "thurs", "tomorrow": "fri"}
	elif current_code == "fri":
		return {"day": "Friday", "code": "fri", "tomorrow": "sat"}
	elif current_code == "sat":
		return {"day": "Saturday", "code": "sat", "tomorrow": "sun"}
	elif current_code == "sun":
		return {"day": "Sunday", "code": "sun", "tomorrow": "mon"}


def get_possible_days():
	possible_days = []

	startday = r.get(app.config['SETTING_PREFIX'] + "startday")
	endday = r.get(app.config['SETTING_PREFIX'] + "endday")

	curday = startday
	cycle = True
	while cycle:
		today = get_day_info(curday)
		possible_days.append(today)
		if today['code'] == endday:
			cycle = False
		else:
			curday = today['tomorrow']

	return possible_days


@app.template_filter('expand_day')
def expand_day(shortcode):
	return get_day_info(shortcode)['day']