from intranet import app, users

from flask import render_template, request, redirect
from flask.ext.login import login_user, logout_user

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template('login.html')

	username = request.form['username']
	password = request.form['password']

	if not username or not password:
		return redirect("/login")

	credentialsCorrect = users.check_password(username, password)

	if credentialsCorrect:
		user = users.get_user(username=username)
		login_user(user)

		return redirect("/")
	else:
		return redirect("/login")

@app.route("/logout")
def logout():
	logout_user()
	return redirect("/")