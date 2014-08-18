import MySQLdb

from intranet.models.group import Group

class GroupTools(object):
	def __init__(self, app):
		self.app = app
		
	def get_cursor(self):
		con = MySQLdb.connect(
				host=self.app.config['XF']['HOST'],
				user=self.app.config['XF']['USER'],
				passwd=self.app.config['XF']['PASS'],
				db=self.app.config['XF']['DBASE']
			)
		return con.cursor()

	def get_group_memberships(self, user):
		cur = self.get_cursor()

		sql = "SELECT g.user_group_id, g.title FROM xf_user_group g WHERE user_group_id IN (SELECT user_group_id FROM xf_user_group_relation WHERE user_id = %s)"

		cur.execute(sql, (user.id,))

		output = []

		for group in cur.fetchall():
			output.append(Group(*group))

		return output