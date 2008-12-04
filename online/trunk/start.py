#!/usr/bin/env python2.5

import sys
import os

try:
    here = __file__
except NameError:
    here = sys.argv[0]

lib = os.path.abspath(os.path.join(os.path.dirname(here), '3rdparty'))
if os.path.isdir(lib):
    sys.path.insert(1, lib)

if len(sys.argv) == 1: # no arguments, lets prepare few for paster (development only)
    sys.argv.append('serve')
    sys.argv.append('--reload')
    sys.argv.append('development.ini')

# run paster
from paste.script import command
command.run()

