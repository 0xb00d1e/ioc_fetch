#!/usr/bin/env python3
  
import os
import sys


sys.path.insert(0, '/home/ioc_fetch/')

activate_this = '/home/ioc_fetch/ioc_fetch/venv/bin/activate_this.py'

exec(open(activate_this).read(), dict(__file__=activate_this))


from ioc_fetch.app import create_app

application = create_app('prod')
