import os
import redis

from flask import Flask
from flask.ext.assets import Bundle, Environment
from flask.ext.login import LoginManager, current_user
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy

from intranet.classes.groups import GroupTools
from intranet.classes.users import UserTools

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")

assets = Environment(app)
db = SQLAlchemy(app)
groups = GroupTools(app)
migrate = Migrate(app, db)
users = UserTools(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

from intranet.models.user import AnonymousUser
lm.anonymous_user = AnonymousUser

@lm.user_loader
def load_user(userid):
	return users.get_user(user_id=userid)

assets.load_path = [
	os.path.join(os.path.dirname(__file__), 'static'),
	os.path.join(os.path.dirname(__file__), 'static', 'bower_components'),
]

assets.register(
	'js_all',
	Bundle(
		'jquery/dist/jquery.min.js',
		'bootstrap/dist/js/bootstrap.min.js',
		output='js_all.js'
	)
)

assets.register(
	'css_all',
	Bundle(
		'css/fonts.css',
		'fontawesome/css/font-awesome.css',
		'bootswatch/sandstone/bootstrap.min.css',
		'css/intranet.css',
		output='css_all.css'
	)

)

r = redis.Redis(host=app.config['REDIS_SERVER'], port=app.config['REDIS_PORT'])

@app.context_processor
def settings_processor():
	def get_setting(setting):
		retval = r.get(app.config['SETTING_PREFIX'] + setting)
		if retval == "False":
			return False
		else:
			return retval
	return dict(setting=get_setting)

from intranet import views, filters

from intranet.models import timeslots, games, music
