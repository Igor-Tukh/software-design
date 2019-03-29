from source.commands.command import Command

import os
import sys


class WordCount(Command):
    """
    wc command, counts number of lines, words and bytes
    """

    def execute(self, variables_environment, previous_output=None):
        if len(self.args) == 0:
            if previous_output is not None:
                if previous_output[-1] != os.linesep:
                    previous_output = previous_output + os.linesep
                lines_number = previous_output.count(os.linesep)
                words_number = len([word for word in previous_output.replace(os.linesep, ' ').split(' ')
                                    if len(word) > 0])
                bytes_number = len(previous_output)
                return ' '.join(map(str, [lines_number, words_number, bytes_number]))
            else:
                raise NotEnoughArgumentsError('wc: not enough arguments')
        result = []
        total = [0, 0, 0]
        file_not_found_errors = []
        for arg in self.args:
            try:
                with open(arg, 'rb') as current_file:
                    text = current_file.read().decode(sys.stdout.encoding)
                    lines_number = text.count(os.linesep)
                    words_number = len([word for word in text.replace(os.linesep, ' ').split(' ')
                                        if len(word) > 0])
                    bytes_number = os.path.getsize(arg)
                    current = [lines_number, words_number, bytes_number]
                    for i in range(3):
                        total[i] += current[i]
                    result.append(' '.join(map(str, current)))
            except FileNotFoundError:
                file_not_found_errors.append('wc: \'{filename}\': No such file'.format(filename=arg))

        if len(file_not_found_errors) > 0:
            raise FileNotFoundError(os.linesep.join(file_not_found_errors))

        if len(self.args) > 1:
            result.append(' '.join(map(str, total)))

        return os.linesep.join(result)


class NotEnoughArgumentsError(Exception):
    """
    Error shell class
    """
    pass
