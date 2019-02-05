from source.commands.command import Command

import os


class WordCount(Command):
    """
    wc command, counts number of lines, words and bytes
    """

    def execute(self, variables_environment, previous_output=None):
        if len(self.args) == 0:
            if previous_output is not None:
                return ' '.join(map(str,
                                    map(len,
                                        [previous_output.split(os.linesep),
                                         previous_output.replace(os.linesep, ' ').split(' '),
                                         previous_output])))
            else:
                raise NotEnoughArgumentsError('wc: not enough arguments')
        result = []
        total = [0, 0, 0]
        for arg in self.args:
            try:
                with open(arg, 'r') as current_file:
                    text = current_file.read()
                    current = list(map(len, [text.split(os.linesep), text.replace(os.linesep, ' ').split(' '), text]))
                    for i in range(3):
                        total[i] += current[i]
                    result.append(' '.join(map(str, current)))
            except FileNotFoundError:
                result.append('wc: \'{filename}\': No such file'.format(filename=arg))

        if len(self.args) > 1:
            result.append(' '.join(map(str, total)))

        return os.linesep.join(result)


class NotEnoughArgumentsError(Exception):
    """
    Error shell class
    """
    pass
