from commands.command import Command


class Assignment(Command):
    """
    Class for assignment commands such as a=4 or b=$a
    """

    def execute(self, variables_environment, previous_output):
        if len(self.args) > 2:  # We have at least 2
            raise TypeError('Unexpected token after assignment')
        variables_environment[self.args[0]] = self.args[1]
        return ''
