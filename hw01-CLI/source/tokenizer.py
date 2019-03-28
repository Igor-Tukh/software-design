class Tokenizer(object):
    """
    Class which consistently splits lines into tokens and stores intermediate data such as quotes info, variables
    environment, tokens and current token.
    """

    class QuotesInfo(object):
        """
        Class which stores information about the current quotes environment.
        """

        def __init__(self):
            self.single_quotes = False
            self.double_quotes = False

        def update(self, character):
            if character in ['\'', '\"']:
                if character == '\'':
                    if not self.double_quotes:
                        self.single_quotes ^= 1
                        return True
                else:
                    if not self.single_quotes:
                        self.double_quotes ^= 1
                        return True
            return False

        def in_quotes(self):
            return self.single_quotes or self.double_quotes

        def substitute_variable(self):
            return not self.single_quotes

    def __init__(self, variables):
        self.quotes_state = self.QuotesInfo()
        self.last_token = ''
        self.tokens = []
        self.variables = variables

    def refresh(self):
        """
        Clear all intermediate data (but not variables environment)
        :return: nothing
        """
        self.quotes_state = self.QuotesInfo()
        self.last_token = ''
        self.tokens = []

    def tokenize(self, line):
        """
        Tokenize line into tokens, substitutes values for environment variables
        :param line: line to tokenize
        :return: nothing
        """

        current_ind = 0
        while current_ind < len(line):
            if line[current_ind] in ['\'', '\"']:
                if not self.quotes_state.update(line[current_ind]):
                    self.last_token += line[current_ind]
                current_ind += 1
            elif not self.quotes_state.in_quotes() and line[current_ind] == '|':
                current_ind = self._process_pipe(current_ind)
            elif line[current_ind] == ' ':
                current_ind = self._process_space(line, current_ind)
            elif line[current_ind] == '$':
                current_ind = self._process_dollar(line, current_ind)
            else:
                self.last_token += line[current_ind]
                current_ind += 1

        if self.quotes_state.in_quotes():
            self.last_token += '\n'
        elif self.last_token != '':
            self.tokens.append(self.last_token)
            self.last_token = ''

    def _process_space(self, line, position):
        while position < len(line) and line[position] == ' ':
            if self.quotes_state.in_quotes():
                self.last_token += ' '
            position += 1

        if self.last_token != '' and not self.quotes_state.in_quotes():
            self.tokens.append(self.last_token)
            self.last_token = ''

        return position

    def _process_pipe(self, position):
        if self.last_token != '':
            self.tokens.append(self.last_token)
            self.last_token = ''
        self.tokens.append('|')
        position += 1

        return position

    def _process_dollar(self, line, position):
        if self.quotes_state.substitute_variable():
            start_index = position + 1
            position += 1
            while position < len(line) and line[position] != ' ' and line[position] != '$':
                position += 1
            name = line[start_index:position]
            if name in self.variables:
                self.last_token += self.variables[name]
            else:
                raise UnknownVariableError('name \'{name}\' is not defined'.format(name=name))
        else:
            self.last_token += '$'
            position += 1

        return position

    def get_tokens(self):
        """
        Returns tokens if quotes are closed
        :return: list of string tokens if quotes are closed and None otherwise  (it means that tokenizing is not over)
        """
        return None if self.quotes_state.in_quotes() else self.tokens


class UnknownVariableError(NameError):
    """
    Shell error class
    """
    pass
