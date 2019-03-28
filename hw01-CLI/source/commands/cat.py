from source.commands.command import Command

import os
import sys


class Cat(Command):
    """
    Cat command, prints all the given files content
    """

    def execute(self, variables_environment, previous_output=None):
        if len(self.args) == 0:
            if previous_output is not None:
                return previous_output
            else:
                raise FileNotFoundError('cat: \'{name}\': No such file or directory'.format(name=previous_output))
        result = []
        for arg in self.args:
            try:
                with open(arg, 'rb') as current_file:
                    result.append(current_file.read().decode(sys.stdout.encoding))
            except FileNotFoundError:
                raise FileNotFoundError('cat: \'{name}\': No such file or directory'.format(name=arg))
        return os.linesep.join(result)
