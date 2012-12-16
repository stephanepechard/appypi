# -*- coding: utf-8 -*-
""" Main appypi controller class. """

# system
import datetime
import os
import pickle
import shutil
import subprocess
import sys
from os.path import join
# appypi
from appypi import settings
from appypi.models import AppypiDatabase, Application
from appypi.pypi import PypiInterface
from appypi.TerminalView import TerminalView
from appypi.utils import create_dir, create_templated_file, bash_file
from appypi.utils import apps_in_path, delete_dir, is_binary


class ApplicationController(object):
    """ Main controller to run appypi. """

    def __init__(self, args):
        create_dir(settings.APPYPI_DIR)
        create_dir(settings.CACHE_DIR)
        self.app_model = None
        self.view = TerminalView()
        self.adb = AppypiDatabase()
        self.pypi = PypiInterface()

        self.command = args['<command>'] if args['<command>'] else None
        self.package = args['<package>'] if args['<package>'] else None
        if args['--requirements']:
            self.requirement = args['--requirements']
        else:
            self.requirement = None

    def run(self):
        """ Launch the app with user-given arguments. """

        # without package list
        if self.command == 'list':
            self.list_apps()
        elif self.command == 'update':
            self.update()
        elif self.command == 'upgrade':
            self.upgrade()
        else:
            packages = self.package
            if packages:
                if self.command == 'install':
                    for package in packages:
                        self.install(package)
                elif self.command == 'remove':
                    self.remove(packages)
                elif self.command == 'show':
                    for package in packages:
                        self.show(package)
                else:
                    message = "Unknown command. Try 'install', " + \
                              "'upgrade', 'remove', 'show', 'list' " + \
                              "or 'update'."
                    self.view.print_error_and_exit(message)

            else:
                if self.requirement:
                    self.install_req()
                else:
                    message = "Please specify a package."
                    self.view.print_error_and_exit(message)

    def install(self, package):
        """ Install the app, based on the user-given name. """

        # check if it is not an uninstallable package
        if package in settings.UNINSTALLABLE_PACKAGES:
            message = "{0} is not installable through appypi, sorry!"\
                        .format(package)
            self.view.print_info(message)
            return

        # check if it is already installed
        if self.adb.app_is_installed(package):
            message = "{0} is already installed.".format(package)
            self.view.print_info(message)
            return

        # find if package exists in pypi
        name = self.find_package(package)
        if not name:
            message = "Can't find {0}".format(package)
            self.view.print_error_and_exit(message)
        else:
            self.view.print_info('Installing...')

        # create ~/.appypi/<package> directory
        self.create_app_dir()
        # create and source boostrap file ~/.appypi/<package>/bootstrap
        self.create_app_bootstrap()
        # create launchers file in ~/bin (depends on what the package defines)
        nb_launchers = self.create_launchers()

        if nb_launchers == 0:
            if self.requirement:
                message = "There's no launcher to be set for this package." \
                          "appypi won't install it..."
                self.view.print_info(message)
            else:
                message = "There's no launcher to be set for this package. " \
                          "It is useless to install it through appypi, " \
                          "as you wouldn't be able to use it. Mission aborted!"
                # clean this mess and quit
                delete_dir(self.app_model.app_dir)
                self.view.print_error_and_exit(message)
        else:
            self.adb.add_app(self.app_model)
            self.view.print_info('Install successful!')

    def install_req(self):
        """ Install a list of package written in a file. """
        req = self.requirement
        try:
            if not is_binary(req):
                lines = None
                with open(req, 'r') as req:
                    lines = req.read()

                for package in lines.split():
                    self.install(package)
            else:
                message = "File {0} is not made of text!".format(req)
                self.view.print_error_and_exit(message)
        except IOError:
            message = "Can't find file {0}".format(req)
            self.view.print_error_and_exit(message)

    def get_package_list(self):
        """ Get list of Pypi packages from pypi website or local cache. """
        if os.path.exists(settings.PACKAGE_CACHE_FILE):
            file_mod_time = os.path.getmtime(settings.PACKAGE_CACHE_FILE)
            mod_datetime = datetime.datetime.fromtimestamp(file_mod_time)
            time_delta = datetime.datetime.now() - mod_datetime
            if time_delta.days > 7:
                message = "Local list of packages is a bit old, updating..."
                self.view.print_info(message)
                self.pypi.update_package_list()
        else:
            self.pypi.update_package_list()

        return pickle.load(open(settings.PACKAGE_CACHE_FILE, 'r'))

    def find_package(self, package):
        """ Try to find the user-given package into pypi repository. """
        message = "Looking for {0}...".format(package)
        self.view.print_info(message)

        found = None
        package_low = package.lower()
        for name in self.get_package_list():
            if package_low == name.lower():
                # found it, can create the model now
                self.app_model = Application(name.lower())
                self.app_model.real_name = name

                # version
                version = self.pypi.last_version(self.app_model)
                self.app_model.installed_version = version
                message = "Found {0} version {1}".format(name, version)
                self.view.print_info(message)

                # set data to the model
                data = self.pypi.release_data(self.app_model, version)
                try:
                    self.app_model.homepage = data['home_page']
                    self.app_model.author = data['author']
                    self.app_model.description = data['description']
                    self.app_model.summary = data['summary']
                except KeyError:
                    pass

                found = name
                break

        return found

    def create_app_dir(self):
        """ Create the app directory. """
        self.app_model.app_dir = join(settings.APPYPI_DIR,
                                              self.app_model.name)
        create_dir(self.app_model.app_dir)

    def create_app_bootstrap(self):
        """ Create the bootstrap file. """
        app_dir = self.app_model.app_dir
        bootstrap = join(app_dir, settings.BOOTSTRAP_NAME)
        tmp = join(settings.TEMPLATE_DIR, settings.BOOTSTRAP_TEMPLATE)
        template = join(os.path.dirname(__file__), tmp)

        # fill substitutes
        substitutes = settings.BOOTSTRAP_SUBS
        substitutes['package'] = self.app_model.name
        if not create_templated_file(bootstrap, template, substitutes):
            message = "Can't create bootstrap file: {0}".format(bootstrap)
            self.view.print_error_and_exit(message)

        # sourcing
        if not bash_file(bootstrap):
            message = "Package install failed!"
            self.view.print_error_and_exit(message)

    def create_launchers(self):
        """ Create the launcher files. """

        venv_bin = join(self.app_model.app_dir, 'venv', 'bin')
        fileslist = os.listdir(venv_bin)
        number_of_binfile = 0
        for binfile in fileslist:
            found_a_binfile = True
            for start in settings.LAUNCHER_EXCLUDE_STARTS:
                if binfile.startswith(start):
                    found_a_binfile = False
                    break

            if found_a_binfile:
                number_of_binfile = number_of_binfile + 1
                self.check_launcher(binfile)
                self.create_launcher(binfile)
                self.app_model.add_binfile(binfile)

        return number_of_binfile

    def check_launcher(self, binfile):
        """ Check if the launcher is installable. """
        apps_in_system = apps_in_path(binfile)

        if apps_in_system:
            # check if in a virtualenv: http://stackoverflow.com/q/1871549
            if hasattr(sys, 'real_prefix'):
                for path in apps_in_system[:]:
                    if path.startswith(sys.prefix) or binfile == 'appypi':
                        # virtualenv and appypi don't count, remove them
                        apps_in_system.remove(path)
            if not len(apps_in_system):
                apps_in_system = None

        if apps_in_system:
            message = "{0} seems to be installed already (pointing to: " \
                      "{1}). Please, remove this version before installing " \
                      "it with appypi, or maybe you can use it." \
                      .format(binfile, ' and '.join(apps_in_system))
            # clean this mess and quit
            delete_dir(self.app_model.app_dir)
            self.view.print_error_and_exit(message)

    def create_launcher(self, binfile):
        """ Create one launcher file. """
        create_dir(settings.BIN_DIR)  # in case it's the first time

        launcher = join(settings.BIN_DIR, binfile)
        tmp = join(settings.TEMPLATE_DIR, settings.BINFILE_TEMPLATE)
        template = join(os.path.dirname(__file__), tmp)

        # fill substitutes
        substitutes = settings.LAUNCHER_SUBS
        app_dir = self.app_model.app_dir
        substitutes['activate'] = join(app_dir, settings.ACTIVATE_FILE)
        substitutes['binfile'] = binfile
        if not create_templated_file(launcher, template, substitutes):
            message = "Can't create launcher file: {0}".format(launcher)
            self.view.print_error_and_exit(message)

        os.chmod(launcher, 0755)  # make it executable

    def remove(self, packages):
        """ Remove some installed apps, based on the user-given names. """

        apps_to_remove = []
        for package in packages:
            app_to_remove = self.adb.app_is_installed(package)
            if app_to_remove:
                apps_to_remove.append(app_to_remove)
            else:
                message = "Package {0} is not installed.".format(package)
                self.view.print_info(message)

        if not apps_to_remove:
            sys.exit()

        # ask for confirmation
        app_names = []
        for app in apps_to_remove:
            app_names.append(app.real_name)

        self.view.print_info("\nThese packages will be REMOVED:\n\n\t{0}\n"
                            .format(" ".join(app_names)))
        cont = self.view.format_question('Do you want to continue? [y/n]')
        confirmation = raw_input(cont)
        if confirmation != 'y':
            return

        for app_to_remove in apps_to_remove:
            # delete app_dir
            shutil.rmtree(app_to_remove.app_dir, True)
            # delete ~/bin/<binfile> files
            if app_to_remove.binfiles:
                binfiles = app_to_remove.binfiles.split(':')
                for binfile in binfiles:
                    os.remove(join(settings.BIN_DIR, binfile))
            # remove from database
            self.adb.remove_app(app_to_remove)

            # user message
            message = "Package {0} has been removed." \
                        .format(app_to_remove.real_name)
            self.view.print_info(message)

    def list_apps(self):
        """ List installed apps on screen. """
        packages = self.adb.installed_packages()
        nb_p = len(packages)
        message = "appypi - {0} installed package{1}" \
                .format(nb_p, 's' if nb_p > 1 else '')
        self.view.print_info(message)
        if not nb_p:
            return

        # compute max_len
        max_len = 0
        for package in packages:
            if max_len < len(package.real_name):
                max_len = len(package.real_name)
        max_len = max(max_len, len('Name'))

        # format output
        separator = '-' * (max_len + 20)
        self.view.print_info(separator)
        message = "{0:{1}} - {2:7} - {3}" \
                .format('Name', max_len, 'Version', 'Summary')
        self.view.print_info(message)
        self.view.print_info(separator)
        for package in packages:
            version = package.installed_version
            message = "{0:{1}} - {2:7} - {3}" \
                    .format(package.real_name, max_len,
                            version, package.summary)
            self.view.print_info(message)

    def upgrade_app(self, app_to_upgrade):
        """ Upgrade an app to the last version. """
        curr_version = app_to_upgrade.installed_version
        last_version = self.pypi.last_version(app_to_upgrade)

        if curr_version == last_version:
            message = "Up to date: {0} ({1})" \
                        .format(app_to_upgrade.real_name, curr_version)
            self.view.print_info(message)
        else:
            # user message
            message = "Upgrading: {0} ({1} => {2})" \
                        .format(app_to_upgrade.real_name,
                                curr_version, last_version)
            self.view.print_info(message)

            # enter the app virtualenv
            exe = join(app_to_upgrade.app_dir,
                       'venv', 'bin', 'activate_this.py')
            execfile(exe, dict(__file__=exe))

            # launch the upgrade
            subprocess.call(['pip', '-q', 'install', '--upgrade',
                            app_to_upgrade.name])

            # upgrade the database
            app_to_upgrade.installed_version = last_version
            self.adb.save()

    def upgrade_all(self):
        """ Upgrade all installed apps to the last version. """
        apps = self.adb.installed_packages()
        for app in apps:
            self.upgrade_app(app)

    def upgrade(self):
        """ Upgrade one or all app. """
        packages = self.package
        if packages:
            for package in packages:
                app_to_upgrade = self.adb.app_is_installed(package)
                if app_to_upgrade:
                    self.upgrade_app(app_to_upgrade)
                else:
                    message = "{0} is not installed.".format(package)
                    self.view.print_info(message)
        else:
            self.upgrade_all()  # upgrade everything

    def update(self):
        """ Update the local database. """
        message = "Updating local database..."
        self.view.print_info(message)
        self.pypi.update_package_list()

    def show(self, package):
        """ Prints info about the given package. """
        app_to_show = self.adb.app_is_installed(package)
        if app_to_show:

            if app_to_show.real_name:
                message = "Package: {0}".format(app_to_show.real_name)
                self.view.print_info(message)
            if app_to_show.installed_version:
                message = "Version: {0}".format(app_to_show.installed_version)
                self.view.print_info(message)
            if app_to_show.author:
                message = u"Author: {0}".format(app_to_show.author)
                self.view.print_info(message)
            if app_to_show.homepage:
                message = "Homepage: {0}".format(app_to_show.homepage)
                self.view.print_info(message)
            if app_to_show.summary:
                message = "Summary: {0}".format(app_to_show.summary)
                self.view.print_info(message)
            if app_to_show.description:
                message = "\nDescription: {0}".format(app_to_show.description)
                self.view.print_info(message)

        else:
            message = "{0} is not installed.".format(package)
            self.view.print_error_and_exit(message)