import os
import sys

from source.interpreter import Interpreter
from source.tokenizer import Tokenizer

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

"""
    Runner. Runs CLI.
    Available commands: 
    1) cat <filenames>
    prints all the given files content
    2) echo <args>
    prints all the arguments
    3) exit 
    exits the CLI
    4) external command <args> 
    runs the external command
    5) pwd
    print current directory full path
    6) wc <filenames>
    counts number of lines, words and bytes
    Also assignments (a=4, b=$a etc) and pipes (|) are available.
"""

if __name__ == '__main__':
    variables = {}
    tokenizer = Tokenizer(variables)
    interpreter = Interpreter(variables)

    print('CLI')

    while True:
        try:
            commands = None
            begin = True
            interpreter.refresh()
            tokenizer.refresh()
            while commands is None:
                if begin:
                    begin = False
                    print('>>', end='')
                print('>', end=' ')
                input_line = input()
                tokenizer.tokenize(input_line)
                tokens = tokenizer.get_tokens()
                while tokens is None:
                    print('>', end=' ')
                    input_line = input()
                    tokenizer.tokenize(input_line)
                    tokens = tokenizer.get_tokens()
                tokenizer.refresh()
                interpreter.interpret(tokens)
                commands = interpreter.get_commands()
            previous_output = None
            for command in commands:
                previous_output = command.execute(variables, previous_output)
                if previous_output is None:
                    exit(0)
            print(previous_output, end='' if previous_output == '' else os.linesep)
        except Exception as e:
            print(str(e))
