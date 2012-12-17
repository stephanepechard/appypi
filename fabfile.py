#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Deployment of appypi. """

# fabric
from fabric.api import env, execute, local
from appypi import __version__ as VERSION
from appypi.utils import remove_launchers


def fast_commit(capture=True):
    """ Fast and dirty commit with common commit message. """
    env.warn_only = True
    local('git commit -am"fast commit through Fabric"')


def push():
    """ Local git push. """
    local("git push")


def deploy():
    """ Commit and push to git servers. """
    execute(fast_commit)
    execute(push)


def reinstall():
    """ Reinstall the project to local virtualenv. """
    local('if [ $(pip freeze | grep appypi | wc -w ) -eq 1 ]; then '
          'pip uninstall -q -y appypi ; fi')
    local('python setup.py sdist')
    local('pip install -q dist/appypi-' + VERSION + '.tar.gz')
    local('rm -rf dist appypi.egg-info MANIFEST')


def install():
    """ Install the project. """
    local('python setup.py install')
    local('rm -rf build')


def tests():
    """ Launch tests. """
    local("rm -rf /tmp/appypi_tmp")
    remove_launchers()

    local("nosetests -v --with-coverage --cover-package appypi tests."
          "test_ApplicationController tests.test_models tests.test_utils")
    local("echo 'y' | nosetests -v --with-coverage --cover-package appypi "
          "tests.test_manual:test_remove")
    local("echo 'n' | nosetests -v --with-coverage --cover-package appypi "
          "tests.test_manual:test_remove_not_confirmed")
    local("nosetests -v --with-coverage --cover-package appypi "
          "tests.test_manual:test_requirement_file")
    local("nosetests -v --with-coverage --cover-package appypi "
          "tests.test_manual:test_requirement_erroneous_file")

    local("coverage html -i -d /tmp/coverage-appypi --omit='appypi/docopt.py'")
    local("coverage erase")


def build_doc():
    """ Build the html documentation. """
    local('cd docs/ && make html')


def clean():
    """ Remove temporary files. """
    local('rm -rf docs/_build/')
    local('find . -name "*.pyc" | xargs rm')


def destroy():
    """ Delete local appypi data. """
    local("rm -rf ~/.appypi")
    remove_launchers()


def upload():
    """ Upload to Pypi. """
    local("python setup.py sdist upload")


def md2rst(in_file, out_file, pipe):
    """ Generate reStructuredText from Makrdown. """
    local("pandoc -f markdown -t rst %s %s > %s" % (in_file, pipe, out_file))


def readme():
    """ Convert Markdown README file to reStructuredText README file. """
    md2rst('README.md', 'README.txt', '| head -n -7')