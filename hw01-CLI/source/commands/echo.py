from source.commands.command import Command


class Echo(Command):
    """
    Echo command, prints all the arguments
    """

    def execute(self, variables_environment, previous_output=None):
        return ' '.join(self.args)
