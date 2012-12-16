# -*- coding: utf-8 -*-
""" Interface with pypi server. """

#system
import pickle
import socket
import xmlrpclib
# appypi
from appypi import settings
from appypi.TerminalView import TerminalView


class PypiInterface(object):
    """ Interface with pypi. """

    def __init__(self):
        self.client = xmlrpclib.ServerProxy(settings.PYPI_SERVER)

    def update_package_list(self):
        """ Update the list of package. """
        view = TerminalView()
        try:
            list_package = self.client.list_packages()
        except socket.gaierror:
            view.print_error_and_exit("Network unreachable!")
        pickle.dump(list_package, open(settings.PACKAGE_CACHE_FILE, 'w'))

    def release_data(self, app_model, version):
        """ Fetch some data of the app. """
        return self.client.release_data(app_model.real_name, version)

    def last_version(self, app_model):
        """ Fetch the last version of the app. """
        versions = self.client.package_releases(app_model.real_name)
        return versions[0]