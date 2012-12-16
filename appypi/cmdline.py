# -*- coding: utf-8 -*-
""" First thing to do: parse user-given arguments. """

# system
import sys
# local
from appypi import __version__ as VERSION
from appypi.ApplicationController import ApplicationController
from appypi.utils import system_check


def docopt_arguments():
    """ Creates beautiful command-line interfaces.
        See https://github.com/docopt/docopt """
    doc = """appypi: sandboxing apps from pypi packages.

    Usage:
           appypi <command> [<package>...]
           appypi install --requirements=<requirements_file>
           appypi list
           appypi -h | --help
           appypi -v | --version

    Options:
        -h, --help      Show this help message and exit.
        -v, --version   Show program's version number and exit.
    """
    from appypi.docopt import docopt
    return docopt(doc, argv=sys.argv[1:], version=VERSION)


def execute():
    """ Main function. """
    system_check()
    controller = ApplicationController(docopt_arguments())
    controller.run()