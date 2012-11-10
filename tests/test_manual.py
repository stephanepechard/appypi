# -*- coding: utf-8 -*-
""" Test suite for some specific user interaction
    needing functions. """

# system
import os
import subprocess
import sys
# appypi
from appypi import settings
from appypi.ApplicationController import ApplicationController
from appypi.cmdline import docopt_arguments, execute
from appypi.models import AppypiDatabase
# tests
from tests.test_ApplicationController import setup_appypi_dir
from tests.test_ApplicationController import teardown_appypi_dir
# nose
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import nottest
from nose.tools import raises
from nose.tools import with_setup
from nose.plugins.capture import Capture


@with_setup(setup_appypi_dir, teardown_appypi_dir)
def test_remove():
    # install first
    sys.argv = ['appypi', 'install', 'projy']
    execute()
    bin_path = os.path.join(os.environ['HOME'], 'bin', 'projy')
    app_path = os.path.join(settings.APPYPI_DIR, 'projy')
    db = AppypiDatabase()
    assert_equal(os.path.isfile(bin_path), True)
    assert_equal(os.path.isdir(app_path), True)
    assert_not_equal(db.app_is_installed('projy'), None)

    # remove then
    sys.argv = ['appypi', 'remove', 'projy']
    execute()
    assert_equal(os.path.isfile(bin_path), False)
    assert_equal(os.path.isdir(app_path), False)
    assert_equal(db.app_is_installed('projy'), None)


@with_setup(setup_appypi_dir, teardown_appypi_dir)
def test_remove_not_confirmed():
    sys.argv = ['appypi', 'install', 'projy']
    execute()
    sys.argv = ['appypi', 'remove', 'projy']
    execute()

