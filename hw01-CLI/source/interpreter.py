from source.commands.assignment import Assignment
from source.commands.cat import Cat
from source.commands.echo import Echo
from source.commands.exit import Exit
from source.commands.external_command import ExternalCommand
from source.commands.pwd import PWD
from source.commands.wc import WordCount


class Interpreter(object):
    """
    Class which consistently interpret commands and stores intermediate data such as variable environment, commands and
    arguments, information about the pipes.
    """
    def __init__(self, variables):
        self.pipe_acceptable = False
        self.last_command = None
        self.args = []
        self.commands = []
        self.variables = variables
        self.last_command = []
        self.pipe_at_the_end = False
        self.command_builders = {'wc': WordCount,
                                 'cat': Cat,
                                 'exit': Exit,
                                 'pwd': PWD,
                                 'echo': Echo,
                                 '=': Assignment}

    def refresh(self):
        """
        Updates all the intermediate data (but not variable environment).
        :return: nothing.
        """
        self.pipe_acceptable = False
        self.last_command = None
        self.args = []
        self.commands = []
        self.last_command = []
        self.pipe_at_the_end = False

    def interpret(self, tokens):
        """
        Interpret all the given tokens. If last token is not pipe becomes available to give commands.
        :param tokens: tokens to interpret
        :return: nothing
        """
        current_ind = 0
        while current_ind < len(tokens):
            if tokens[current_ind] == '|':
                self._process_pipe()
            else:
                self._process_command(tokens[current_ind])
            current_ind += 1

        if len(tokens) > 0 and tokens[-1] == '|':
            self.pipe_at_the_end = True
        elif len(tokens) > 0:
            self.pipe_at_the_end = False
            self._build_command()

    def get_commands(self):
        """
        Return all the interpreted commands.
        :return: commands if last token was not pipe and None otherwise (it means that interpretation is not over)
        """
        if self.pipe_at_the_end:
            return None
        return self.commands

    def _build_command(self):
        if self.last_command in self.command_builders:
            self.commands.append(self.command_builders[self.last_command](self.args))
        else:
            self.commands.append(ExternalCommand([self.last_command] + self.commands))
        self.last_command = None
        self.args = []
        self.pipe_acceptable = False

    def _process_pipe(self):
        if not self.pipe_acceptable:
            raise UnexpectedTokenError('Unexpected token |')

        self._build_command()
        self.pipe_acceptable = False

    def _process_command(self, token):
        if not self.pipe_acceptable:
            sides = token.split('=')
            if len(sides) == 2:
                self.last_command = '='
                self.args = sides
            else:
                self.last_command = token
            self.pipe_acceptable = True
        else:
            self.args.append(token)


class UnexpectedTokenError(SyntaxError):
    """
    Shell error class
    """
    pass
