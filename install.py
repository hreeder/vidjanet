#!/usr/bin/env python
from intranet import app, r

pfix = app.config['SETTING_PREFIX']

print "[redis] Writing Base Config"
r.set(pfix+"eventno", 0)
r.set(pfix+"startday", "mon")
r.set(pfix+"endday", "fri")
r.set(pfix+"RvB", "False")
print "[redis] Base Config Written"


print "Install Complete"
