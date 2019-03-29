from source.tokenizer import Tokenizer, UnknownVariableError

import os
import pytest


def get_tokens(line):
    tokenizer = Tokenizer({})
    tokenizer.tokenize(line)
    return tokenizer.get_tokens()


def test_one_line_tokenize():
    with pytest.raises(UnknownVariableError):
        get_tokens('echo $a')
    assert get_tokens('echo \'a\'') == ['echo', 'a']
    assert get_tokens('exit') == ['exit']
    assert get_tokens('echo 239 | wc') == ['echo', '239', '|', 'wc']
    assert get_tokens('echo 239 | echo | cat | wc') == ['echo', '239', '|', 'echo', '|', 'cat', '|', 'wc']
    assert get_tokens('a=3 \'') is None


def get_tokens_many_lines(lines):
    tokenizer = Tokenizer({})
    result = []
    for line in lines:
        tokenizer.tokenize(line)
        tokens = tokenizer.get_tokens()
        if tokens is not None:
            result += tokens
            tokenizer.refresh()
    return result


def test_several_lines_tokenize():
    assert get_tokens_many_lines(['echo a |', 'wc']) == ['echo', 'a', '|', 'wc']
    assert get_tokens_many_lines(['a=3 \'', 'a\'']) == ['a=3', '{s}a'.format(s=os.linesep)]
    assert get_tokens_many_lines(['a=3 \"', 'a\"']) == ['a=3', '{s}a'.format(s=os.linesep)]


if __name__ == '__main__':
    test_several_lines_tokenize()
