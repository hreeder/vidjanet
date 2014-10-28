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

Known Issues
==
Current XenForo authentication does not support any external authentication methods (ie Facebook or Steam).

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
 - Support for XenForo External Authentication
 - Other types of forums for authentication
 - Internal Authentication
 - Tournament Planning