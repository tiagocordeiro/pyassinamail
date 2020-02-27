#!/usr/bin/env python

CONFIG_STRING = """# Basic settings
DYNACONF_FILE_ID="1vW0NDxmZcQ-Gna9LY6vnsjDm6hVc55QSOt9VGtTAnds"
"""

# Writing our configuration file to '.env'
with open('.env', 'w') as configfile:
    configfile.write(CONFIG_STRING)
