from source.commands.echo import Echo
from source.commands.wc import WordCount
from source.interpreter import Interpreter, UnexpectedTokenError

import pytest


def get_commands(tokens):
    interpreter = Interpreter({})
    interpreter.interpret(tokens)
    return interpreter.get_commands()


def test_raises():
    with pytest.raises(UnexpectedTokenError):
        get_commands(['|'])


def test_one_command():
    commands = get_commands(['echo', '123', '|', 'wc'])
    assert len(commands) == 2
    assert isinstance(commands[0], Echo)
    assert commands[0].args == ['123']
    assert isinstance(commands[1], WordCount)
    assert commands[1].args == []


def test_one_command_with_pipe_at_the_end():
    commands = get_commands(['echo', '123', '|'])
    assert commands is None


def test_several_commands():
    interpreter = Interpreter({})
    interpreter.interpret(['echo', '123', '|'])
    assert interpreter.get_commands() is None
    interpreter.interpret(['wc'])
    commands = interpreter.get_commands()
    assert len(commands) == 2
    assert isinstance(commands[0], Echo)
    assert commands[0].args == ['123']
    assert isinstance(commands[1], WordCount)
    assert commands[1].args == []
