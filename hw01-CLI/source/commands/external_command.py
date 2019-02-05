from source.commands.command import Command
from subprocess import check_output

import subprocess


class ExternalCommand(Command):
    """
    External command class, runs the external command
    """

    def execute(self, variables_environment, previous_output):
        result = check_output(self.args, stderr=subprocess.STDOUT).decode("utf-8")
        return '' if result is None else result
