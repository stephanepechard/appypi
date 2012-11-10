# -*- coding: utf-8 -*-
""" Test suite for the main appypi controller class. """

# system
import os
import shutil
import subprocess
import sys
# appypi
from appypi import settings
from appypi.ApplicationController import ApplicationController
from appypi.cmdline import docopt_arguments, execute
from appypi.models import AppypiDatabase
from appypi.utils import remove_launchers
# nose
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import nottest
from nose.tools import raises
from nose.tools import with_setup
from nose.plugins.capture import Capture


# setups/teardowns
def teardown_appypi_dir():
    remove_launchers()
    if os.path.exists(settings.APPYPI_DIR):
        shutil.rmtree(settings.APPYPI_DIR, True)


def setup_appypi_dir():
    teardown_appypi_dir()
    settings.APPYPI_DIR = os.path.join('/tmp', 'appypi_tmp')
    settings.APPYPI_DB_PATH = os.path.join(settings.APPYPI_DIR, 'appypi.sqlite')
    settings.CACHE_DIR = os.path.join(settings.APPYPI_DIR, 'appypi_cache')
    settings.PACKAGE_CACHE_FILE = os.path.join(settings.APPYPI_DIR, 'appypi_package_cache.dump')
    settings.BOOTSTRAP_SUBS = { 'package': None, 'venv': 'venv',
                                'cache_dir': settings.CACHE_DIR }


# tests
@with_setup(setup_appypi_dir, teardown_appypi_dir)
def test_install():
    sys.argv = ['appypi', 'install', 'projy']
    execute()
    bin_path = os.path.join(os.environ['HOME'], 'bin', 'projy')
    app_path = os.path.join(settings.APPYPI_DIR, 'projy')
    assert_equal(os.path.isfile(bin_path), True)
    assert_equal(os.path.isdir(app_path), True)


@with_setup(setup_appypi_dir, teardown_appypi_dir)
def test_list_and_show():
    sys.argv = ['appypi', 'install', 'projy']
    execute()
    sys.argv = ['appypi', 'list']
    execute()
    sys.argv = ['appypi', 'show', 'projy']
    execute()


@with_setup(setup_appypi_dir, teardown_appypi_dir)
def test_upgrade_all():
    sys.argv = ['appypi', 'install', 'projy']
    execute()
    sys.argv = ['appypi', 'upgrade']
    execute()


@with_setup(setup_appypi_dir, teardown_appypi_dir)
def test_real_upgrade():
    sys.argv = ['appypi', 'install', 'projy']
    execute()
    sys.argv = ['appypi', 'install', 'fabric']
    execute()

    # enter the fabric virtualenv
    exe = os.path.join(settings.APPYPI_DIR, 'fabric', 'venv', 'bin', 'activate_this.py')
    execfile(exe, dict(__file__=exe))
    # launch the downgrade
    subprocess.call(['pip', '-q', 'install', 'fabric==1.4.0'])
    # change the database
    db = AppypiDatabase()
    app = db.app_is_installed('fabric')
    app.installed_version = '1.4.0'
    db.save()

    # run the update
    sys.argv = ['appypi', 'upgrade', 'fabric']
    execute()
    # test
    app2 = db.app_is_installed('fabric')
    assert_not_equal(app2.installed_version, '1.4.0')


@with_setup(setup_appypi_dir, teardown_appypi_dir)
def test_upgrade_uninstalled_package():
    sys.argv = ['appypi', 'upgrade', 'NOT_INSTALLED_PACKAGE']
    execute()


@raises(SystemExit)
@with_setup(setup_appypi_dir, teardown_appypi_dir)
def test_show_unknown_package():
    sys.argv = ['appypi', 'show', 'NOT_INSTALLED_PACKAGE']
    execute()


@raises(SystemExit)
@with_setup(setup_appypi_dir, teardown_appypi_dir)
def test_remove_not_installed_package():
    sys.argv = ['appypi', 'remove', 'projy']
    execute()


@raises(SystemExit)
@with_setup(setup_appypi_dir, teardown_appypi_dir)
def test_install_unknown_package():
    sys.argv = ['appypi', 'install', 'NOT_INSTALLED_PACKAGE']
    execute()


@raises(SystemExit)
def test_install_without_package():
    sys.argv = ['appypi', 'install']
    execute()


@raises(SystemExit)
def test_unknown_command():
    sys.argv = ['appypi', 'NOT_A_COMMAND', 'plop']
    execute()


def test_init():
    arguments = {'--help': False, '--version': False,
                 '<command>': 'install', '<package>': None, 'list': False}
    controller = ApplicationController(arguments)
    assert_equal(controller.arguments, arguments)
    assert_not_equal(controller.view, None)


@with_setup(setup_appypi_dir, teardown_appypi_dir)
def test_update():
    sys.argv = ['appypi', 'update']
    execute()


#def setup_no_network():
    #subprocess.call(['sudo', '/etc/init.d/networking', 'stop'])


#def teardown_no_network():
    #subprocess.call(['sudo', '/etc/init.d/networking', 'start'])


#@with_setup(setup_no_network, teardown_no_network)
#@raises(SystemExit)
#def test_no_network():
    #sys.argv = ['appypi', 'install', 'projy']
    #controller = ApplicationController(docopt_arguments())
    #controller.run()
