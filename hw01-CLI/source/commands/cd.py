import os

from source.commands.command import Command


class Cd(Command):
    """
    cd command, print content of current directory
    """

    def execute(self, variables_environment, previous_output):
        if previous_output is None:
            if len(self.args) > 0:
                os.chdir(os.path.join(os.getcwd(), self.args[0]))
            else:
                os.chdir(os.path.expanduser('~'))
        return ""
