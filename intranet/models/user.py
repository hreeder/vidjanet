from flask.ext.login import AnonymousUserMixin, UserMixin

class User(UserMixin):
	def __init__(self, id, username):
		self.id=id
		self.username=username

	def get_id(self):
		return self.id

	def get_groups(self):
		from intranet import groups
		return groups.get_group_memberships(self)

	def is_admin(self):
		from intranet import users
		return users.is_user_admin(self)

class AnonymousUser(AnonymousUserMixin):
	def is_admin(self):
		return False