# -*- coding: utf-8 -*-
""" Files and directories helpers. """

# system
import os
import shutil
import subprocess
from string import Template
# appypi
from appypi import settings
from appypi.TerminalView import TerminalView


def create_dir(directory):
    """ Create a directory on the user file system. """
    if not os.path.isdir(directory):
        os.mkdir(directory, 0755)


def delete_dir(directory):
    """ Delete a directory of the user file system. """
    if os.path.isdir(directory):
        shutil.rmtree(directory, True)


def create_templated_file(target, template, substitutes):
    """ Create a file from a template, based on a substitutes dictionary. """
    creation = False
    try:
        with open(target, 'w') as dst:
            with open(template, 'r') as src:
                line = Template(src.read())
                dst.write(line.safe_substitute(substitutes))
        creation = True
    except IOError:
        creation = False

    return creation


def bash_file(file_path):
    """ Launch bash on a file of the file system. """
    success = False
    if os.path.isfile(file_path):
        path = os.path.dirname(os.path.realpath(file_path))
        os.chdir(path)
        try:
            subprocess.check_call(["bash", file_path])
            success = True
        except subprocess.CalledProcessError:
            success = False

    return success


def apps_in_path(program):
    """ Return path of a command, or None if command is not found. """
    def is_exe(fpath):
        """ Is this an executable file? """
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    exe_list = []
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                exe_list.append(exe_file)

    if not len(exe_list):
        exe_list = None

    return exe_list


def system_check():
    """ Check the system for needed tools. """
    view = TerminalView()
    # virtualenv should be usable
    if not apps_in_path('virtualenv'):
        message = "Virtualenv is not installed for your user. " \
                  "Please, install it with: pip install --user virtualenv"
        view.print_error_and_exit(message)

    # bash should be usable
    if not apps_in_path('bash'):
        message = "bash is not installed on your system. Please, install it."
        view.print_error_and_exit(message)


def delete_file(filepath):
    """ Securely delete a file. """
    if os.path.exists(filepath) and os.path.isfile(filepath):
        os.remove(filepath)


def remove_launchers():
    """ Erase all files detected as launchers. appypi may miss some if
        the user modified them at some point. """
    if os.path.exists(settings.BIN_DIR):
        binfiles = os.listdir(settings.BIN_DIR)  # list everything in bin dir
        for binfile in binfiles:
            path = os.path.join(settings.BIN_DIR, binfile)  # full path
            if os.path.exists(path) and os.path.isfile(path):
                to_remove = False
                with open(path) as pathfile:
                    # look for appypi-specific line
                    for line in pathfile.readlines():
                        if line == settings.BIN_HEADER + '\n':
                            to_remove = True
                            break

                if to_remove:
                    delete_file(path)  # remove the file


def is_binary(filepath):
    """ Determine if a file is text or binary. """
    charmap = map(chr, [7, 8, 9, 10, 12, 13, 27] + range(0x20, 0x100))
    textchars = ''.join(charmap)
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
    is_binary_string(open(filepath).read(1024))