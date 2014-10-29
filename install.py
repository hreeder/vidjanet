#!/usr/bin/env python
print "+-------- Welcome to VidjaNet --------+"
print "|     LAN Party Intranet Software     |"
print "|              Installer              |"
print "|                                     |"
print "|     github.com/hreeder/vidjanet     |"
print "+-------------------------------------+"

print ""
print "Please make sure you are running this script in the environment you wish to install all requirements."
print "Are you in the correct environment (Y/N) "

# TODO: pip install -r requirements.txt

# Config Generation
config = [
	{
		"parameter": "REDIS_SERVER",
		"description": "IP Address or FQDN of your redis server",
		"default": "localhost"
	},
	{
		"parameter": "REDIS_PORT",
		"description": "Port of your redis server"
	},
	{
		"parameter": "SETTING_PREFIX",
		"description": "Prefix for any settings to be inserted into redis"
	},
	{
		"parameter": "DB_DIALECT",
		"description": "Dialect for your Database, supports anything SQLAlchemy supports - eg 'mysql', 'sqlite', 'postgres'",
		"default": "sqlite"
	},
	{
		"parameter": "DB_SERVER",
		"description": "Server for your SQLAlchemy Database. Not required for sqlite"
	},
	{
		"parameter": "DB_NAME",
		"description": "Name for your SQLAlchemy Database. For sqlite input the path to db file"
	},
	{
		"parameter": "DB_USER",
		"description": "Username for your SQLAlchemy Database. Not required for sqlite"
	},
	{
		"parameter": "XF/HOST",
		"description": "MySQL Hostname where your XenForo database is located",
		"default": "localhost"
	},
	{
		"parameter": "XF/USER",
		"description": "MySQL User with access to your XenForo database"
	},
	{
		"parameter": "XF/PASS",
		"description": "MySQL Password for user with access to your XenForo database",
		"type": "password"
	},
	{
		"parameter": "XF/DBASE",
		"description": "MySQL Database Name for your XenForo database"
	},
	{
		"parameter": "MUSIC_UPLOAD_FOLDER",
		"description": "Choose a folder where you wish to store any uploaded song requests (Absolute or relative to install.py)",
		"default": "/uploads/music/"
	},
	{
		"parameter": "MUSIC_ALLOWED_EXTENSIONS",
		"description": "What file types will you allow for music files? Seperate with spaces",
		"default": "mp3 m4a ogg flac"
	},
	{
		"parameter": "DOWNLOAD_UPLOAD_FOLDER",
		"description": "Choose a folder where you wish to store files for download",
		"default": "/uploads/files"
	}
]

for item in config:
	print "\r\n"
	print "Config Value: " + item['parameter']
	print item['description']
	if "default" in item:
		print "Default: " + item['default']
	print "app.config['" + item['parameter'] + "'] = "

	input = "" # TODO: Get User Input (detect if type is password too)

	if input:
		item['value'] = input
	elif "default" not in item:
		print "I'm sorry, I require a value for that entry!"
	else:
		item['value'] = item['default']

print config

print "\r\nEnable Sentry? (Y/N) "
if sentry:
	print "app.config['SENTRY_DSN'] = "

from intranet import app, r

pfix = app.config['SETTING_PREFIX']

print "[redis] Writing Base Config"
r.set(pfix+"eventno", 0)
r.set(pfix+"startday", "mon")
r.set(pfix+"endday", "fri")
r.set(pfix+"RvB", "False")
print "[redis] Base Config Populated"


print "Install Complete"
print "Please now configure your preferred webserver, and head to /admin/settings in the app to finish setup"