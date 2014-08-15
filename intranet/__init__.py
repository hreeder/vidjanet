import os

from flask import Flask
from flask.ext.assets import Bundle, Environment
from flask.ext.login import LoginManager, current_user

from intranet.classes.users import UserTools

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")

assets = Environment(app)
users = UserTools(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

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