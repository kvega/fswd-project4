#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/CatalogApp/CatalogApp/src/")

from application import app as application
application.secret_key = 'super_duper_secret_key'

