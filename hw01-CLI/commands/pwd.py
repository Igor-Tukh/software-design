from commands.command import Command

import os


class PWD(Command):
    """
    pwd command, print current directory full path
    """

    def execute(self, variables_environment, previous_output=None):
        return os.getcwd()
