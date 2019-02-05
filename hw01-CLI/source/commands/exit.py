from source.commands.command import Command


class Exit(Command):
    """
    Exit command, just exists the CLI
    """

    def execute(self, variables_environment, previous_output=None):
        if previous_output is not None:
            self.args += [previous_output]
        if len(self.args) > 0:
            return 1  # just not None
        return None
