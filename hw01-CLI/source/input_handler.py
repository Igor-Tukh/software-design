import os

from source.interpreter import Interpreter
from source.tokenizer import Tokenizer


class InputHandler(object):
    """
    InputHandler handles input, line-by-line and stores tokenizer and interpreter instances.
    """
    def __init__(self):
        self.variables = {}
        self.tokenizer = Tokenizer(self.variables)
        self.interpreter = Interpreter(self.variables)
        self.begin = False

        print('CLI')
        print('>>>', end=' ')

    def process_input(self, input_line):
        """
        Processes give line
        :param input_line: line to process
        :return: nothing
        """
        try:
            self.tokenizer.tokenize(input_line)
            tokens = self.tokenizer.get_tokens()
            if tokens is None:
                print('>', end=' ')
                return
            self.tokenizer.refresh()
            self.interpreter.interpret(tokens)
            commands = self.interpreter.get_commands()
            if commands is None:
                print('>', end=' ')
                return
            previous_output = None
            for command in commands:
                previous_output = command.execute(self.variables, previous_output)
                if previous_output is None:
                    exit(0)
            print(previous_output, end='' if previous_output == '' else os.linesep)
        except Exception as e:
            print(str(e))
        self.interpreter.refresh()
        self.tokenizer.refresh()
        print('>>>', end=' ')



