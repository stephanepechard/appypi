# -*- coding: utf-8 -*-
""" Test suite for the utils.py file. """

# system
import os
import sys
import uuid
# appypi
from appypi import settings
from appypi.utils import create_dir, bash_file
# nose
from nose.tools import with_setup
from nose.tools import raises
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import nottest


def test_create_dir():
    uid = uuid.uuid4()
    dir_path = os.path.join('/tmp', uid.hex)
    assert_equal(os.path.isdir(dir_path), False)
    create_dir(dir_path)
    assert_equal(os.path.isdir(dir_path), True)


def test_source_not_bash_file():
    uid = uuid.uuid4()
    dir_path = os.path.join('/tmp', uid.hex)
    sourced = bash_file(dir_path)
    assert_equal(sourced, False)

