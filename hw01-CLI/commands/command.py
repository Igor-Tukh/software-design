from abc import ABCMeta, abstractmethod


class Command(object, metaclass=ABCMeta):
    """
    Base abstract class for all the commands.
    New commands could be added by overriding this class and adding them into the interpreter.
    """

    def __init__(self, args):
        self.args = args

    @abstractmethod
    def execute(self, variables_environment, previous_output):
        pass
