# -*- coding: utf-8 -*-
""" Main appypi controller class. """

# system
from blessings import Terminal
import sys


class TerminalView(object):
    """ Terminal view to basic CLI information. """

    def __init__(self):
        self.term = Terminal()

    def print_error_and_exit(self, message):
        """ Print an error in red and exits the program. """
        sys.exit(self.term.bold_red('[ERROR] ' + message))

    def print_info(self, message):
        """ Print an informational text. """
        #print(self.term.bold('[INFO] ') + message)
        print(message)

    def format_question(self, message):
        """ Return an info-formatted string. """
        return self.term.bold(message)