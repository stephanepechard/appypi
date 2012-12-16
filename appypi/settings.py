# -*- coding: utf-8 -*-
""" appypi setup.py script """

# system
import os
from os.path import join


# global
DEBUG = False
PYPI_SERVER = 'http://pypi.python.org/pypi'

# installation
APPYPI_DIR = join(os.environ['HOME'], '.appypi')
APPYPI_DB_PATH = join(APPYPI_DIR, 'appypi.sqlite')
CACHE_DIR = join(APPYPI_DIR, 'appypi_cache')
PACKAGE_CACHE_FILE = join(APPYPI_DIR, 'appypi_package_cache.dump')
UNINSTALLABLE_PACKAGES = ['pip', 'python', 'virtualenv']

# bootstrap
BOOTSTRAP_NAME = 'bootstrap'
BOOTSTRAP_SUBS = {'package': None,
                  'venv': 'venv',
                  'cache_dir': CACHE_DIR}

# launchers
BIN_DIR = join(os.environ['HOME'], 'bin')
ACTIVATE_FILE = 'venv/bin/activate'
BIN_HEADER = "# appypi-installed application launcher, DO NOT EDIT!"
LAUNCHER_SUBS = {'activate': None, 'binfile': None, 'header': BIN_HEADER}
LAUNCHER_EXCLUDE_STARTS = ['activate', 'easy_install', 'pip', 'python']

# templates
TEMPLATE_DIR = 'templates'
BOOTSTRAP_TEMPLATE = 'bootstrapfile_template'
BINFILE_TEMPLATE = 'binfile_template'