from source.commands.command import Command

import subprocess
import sys


class ExternalCommand(Command):
    """
    External command class, runs the external command
    """

    def execute(self, variables_environment, previous_output):
        try:
            if previous_output is None or previous_output == '':
                result = subprocess.run(self.args,
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        check=True)
            else:
                result = subprocess.run(self.args,
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stdin=previous_output,
                                        check=True)
            return result.stdout.decode(sys.stdout.encoding)
        except subprocess.CalledProcessError as e:
            raise ExternalCommandException(e.stderr.decode(sys.stderr.encoding))
        except FileNotFoundError:
            raise ExternalCommandException('{}: command not found'.format(self.args[0]))


class ExternalCommandException(Exception):
    """
    Error shell class
    """
    pass
