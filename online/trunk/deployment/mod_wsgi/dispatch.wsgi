# vim: ft=python
import site
import sys
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_dir)

lib = os.path.join(root_dir, '3rdparty')
if os.path.isdir(lib):
    sys.path.insert(1, lib)
    #site.addsitedir(lib)

# Load the Pylons application
from paste.deploy import loadapp
application = loadapp("config:%s/production.ini" % root_dir)
