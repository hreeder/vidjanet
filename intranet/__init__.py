import os

from flask import Flask
from flask.ext.assets import Bundle, Environment
from flask.ext.login import LoginManager, current_user

from intranet.classes.groups import GroupTools
from intranet.classes.users import UserTools

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")

assets = Environment(app)
users = UserTools(app)
groups = GroupTools(app)

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
		'bootswatch/sandstone/bootstrap.min.css',
		'css/intranet.css',
		output='css_all.css'
	)

)

from intranet import views