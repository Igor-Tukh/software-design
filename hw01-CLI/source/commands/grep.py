from source.commands.command import Command

import argparse
import re
import os


class Grep(Command):
    """
        Grep command class. Print lines matching a pattern.
        Supports options:

        -i
            register insensitivity

        -w
            search only whole-matching words

        -A N
            print N lines after matching line
    """

    def execute(self, variables_environment, previous_output):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', help='register insensitivity', action='store_true')
        parser.add_argument('-w', help='search only whole-matching words', action='store_true')
        parser.add_argument('-A', help='print N lines after matching line', type=int, metavar='N')

        try:
            args, others = parser.parse_known_args(self.args)
        except Exception as e:
            raise GrepArgumentParseException('grep: error during parsing arguments: {e}'.format(e=e.__cause__))

        from_text = False
        if previous_output is not None and previous_output != '':
            others.append(previous_output)
            from_text = True

        if len(others) < 2:
            raise GrepArgumentParseException('grep: too few parameters')

        text = others[-1].split(os.linesep) if from_text else Grep._read_file_or_throw(others[-1])
        pattern = r'\b{p}\b'.format(p=others[0]) if args.w else others[0]
        result_re = re.compile(pattern, 0 if not args.i else re.IGNORECASE)
        N = args.A if args.A is not None else 0
        lines = [os.linesep.join(text[ind:min(ind + N + 1, len(text))]) for ind, line in enumerate(text)
                 if re.search(result_re, line) is not None]
        return os.linesep.join(lines)

    @staticmethod
    def _read_file_or_throw(filename):
        try:
            with open(filename, 'r') as reading_file:
                return [line.replace(os.linesep, '') for line in reading_file.readlines()]
        except FileNotFoundError:
            raise GrepArgumentParseException('grep: {name}: No such file or directory'.format(name=filename))


class GrepArgumentParseException(Exception):
    """
    Error shell class
    """
    pass
