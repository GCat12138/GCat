#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/GCat/")

activate_this = '/var/www/GCat/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from app import create_app
application = create_app("default")

