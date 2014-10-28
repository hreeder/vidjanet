VidjaNet
=

VidjaNet is a LAN Party Intranet Site

Requirements
==
Python (Developed in 2.7 - untested on any other platform)
SQLAlchemy Supported Database Server
XenForo (More forums/auth methods coming later - open or comment on an issue if there is one you would like to see)
 - Current Implementation only supports MySQL for XenForo database
Redis (For storing site settings)

Installation
==
Run the following
```
virtualenv .env
source .env/bin/activate
python install.py
```
And follow the installer prompts to generate your config file and populate your initial redis config.

TODO
==
 - Other types of forums for authentication
 - Internal Authentication
 - Tournament Planning