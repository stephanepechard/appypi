# -*- coding: utf-8 -*-
""" Test suite for the models.py file. """

# system
import os
import sys
# appypi
from appypi import settings
from appypi.ApplicationController import ApplicationController
from appypi.models import AppypiDatabase, Application
from appypi.utils import create_dir
# tests
from tests.test_ApplicationController import setup_appypi_dir, teardown_appypi_dir
# nose
from nose.tools import with_setup
from nose.tools import raises
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import nottest


def setup_appypi_dir_models():
    setup_appypi_dir()
    create_dir(settings.APPYPI_DIR)


@with_setup(setup_appypi_dir_models, teardown_appypi_dir)
def test_app_is_not_installed():
    db = AppypiDatabase()
    app = Application('application')
    app.add_binfile('binfile')
    db.add_app(app)
    assert_equal(db.app_is_installed('app'), None)


@with_setup(setup_appypi_dir_models, teardown_appypi_dir)
def test_app_is_installed():
    db = AppypiDatabase()
    app = Application('application')
    app.add_binfile('binfile1')
    app.add_binfile('binfile2')
    db.add_app(app)
    assert_not_equal(db.app_is_installed('application'), None)


@with_setup(setup_appypi_dir_models, teardown_appypi_dir)
def test_create_db():
    db = AppypiDatabase()
    app = Application('application')
    app.add_binfile('binfile1')
    app.add_binfile('binfile2')
    db.add_app(app)
    print(app)
    assert_equal(os.path.isfile(settings.APPYPI_DB_PATH), True)
