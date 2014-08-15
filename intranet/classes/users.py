import MySQLdb

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
		else:
			return False