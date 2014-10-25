import hashlib
import MySQLdb

from flask import flash, redirect
from flask.ext.login import current_user
from functools import wraps
from phpass import PasswordHash

from intranet.models.user import User

class UserTools(object):
	"""Tools for retrieving user objects"""

	def __init__(self, app):
		self.app=app

	def get_cursor(self):
		con = MySQLdb.connect(
				host=self.app.config['XF']['HOST'],
				user=self.app.config['XF']['USER'],
				passwd=self.app.config['XF']['PASS'],
				db=self.app.config['XF']['DBASE']
			)
		return con.cursor()
	
	def get_user(self, user_id=None, username=None):
		cur = self.get_cursor()

		sql = "SELECT user_id, username FROM xf_user WHERE "
		queryargs=[]

		if user_id:
			sql += "user_id = %s"
			queryargs.append(user_id)

		if username:
			if user_id:
				sql += " AND "
			sql += "username = %s"
			queryargs.append(username)

		cur.execute(sql, tuple(queryargs))

		user=cur.fetchone()

		if not user:
			return False

		return User(*user)

	def check_password(self, username, password):
		cur = self.get_cursor()
		hasher = PasswordHash()

		sql = "SELECT scheme_class, data FROM xf_user_authenticate WHERE user_id = (SELECT user_id FROM xf_user WHERE username=%s)"
		cur.execute(sql, (username,))

		row = cur.fetchone()

		if not row:
			return False

		scheme, data = row

		if scheme == "XenForo_Authentication_Core12":
			hash = data.split(";")[1].split('"')[1]
			return hasher.check_password(str(password), str(hash))
		elif scheme == "XenForo_Authentication_vBulletin":
			hash = data.split(";")[1].split('"')[1]
			salt = data.split(";")[3].split('"')[1]
			
			outer = hashlib.md5()
			inner = hashlib.md5()

			inner.update(str(password))
			outer.update(inner.hexdigest())
			outer.update(str(salt))

			return outer.hexdigest() == hash
		else:
			flash("Login Error - Please Contact Skull - SCHEME NOT RECOGNISED", "danger")
			return False

	def is_user_admin(self, user):
		return self.app.config['ADMIN_GROUP_ID'] in [int(group.id) for group in user.get_groups()]

def admin(func):
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if current_user.is_admin():
			return func(*args, **kwargs)
		flash("You are not an admin. If this is an error, please contact Skull <3")
		return redirect("/")
	return decorated_view