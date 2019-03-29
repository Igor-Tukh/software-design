from source.commands.assignment import Assignment
from source.commands.cat import Cat
from source.commands.echo import Echo
from source.commands.exit import Exit
from source.commands.external_command import ExternalCommand, ExternalCommandException
from source.commands.pwd import PWD
from source.commands.wc import WordCount


import os
import platform
import pytest


def test_assignments():
    variables = {}
    cmd = Assignment(['a', '1'])
    cmd.execute(variables, '')
    assert 'a' in variables and variables['a'] == '1'


def test_cat():
    cmd = Cat([])
    assert cmd.execute({}, '123') == '123'
    cmd = Cat([os.path.join(os.getcwd(), 'hw01-CLI', 'tests', 'resources', '1.txt')])
    assert cmd.execute({}, '') == '1'
    assert cmd.execute({}, '123') == '1'
    cmd = Cat([os.path.join(os.getcwd(), 'hw01-CLI', 'tests', 'resources', '1.txt'),
               os.path.join(os.getcwd(), 'hw01-CLI', 'tests', 'resources', '2.txt')])
    assert cmd.execute({}, '') == '1' + os.linesep + '1' + os.linesep + '2'


def test_echo():
    cmd = Echo([])
    assert cmd.execute({}, '1') == ''
    cmd = Echo(['2', '3', '9'])
    assert cmd.execute({}, '1') == '2 3 9'


def test_exit():
    cmd = Exit([])
    assert cmd.execute({}, '123') is ''
    cmd = Exit([])
    assert cmd.execute({}, None) is None


def test_external_command():
    if platform.system() == 'Windows':
        cmd = ExternalCommand(['dir'])
    else:
        cmd = ExternalCommand(['ls'])
    try:
        print(cmd.execute({}, ''))
    except ExternalCommandException as e:
        pytest.fail('Unexpected error: {}'.format(e))


def test_pwd():
    cmd = PWD(['ls'])
    assert cmd.execute({}, 'a') == os.getcwd()  # it is bad check, bad the only one possible :)


def test_wc():
    first_path = os.path.join(os.getcwd(), 'hw01-CLI', 'tests', 'resources', '1.txt')
    second_path = os.path.join(os.getcwd(), 'hw01-CLI', 'tests', 'resources', '2.txt')
    third_path = os.path.join(os.getcwd(), 'hw01-CLI', 'tests', 'resources', '3.txt')
    with pytest.raises(FileNotFoundError):
        cmd = WordCount([third_path])
        cmd.execute({}, '')
    cmd = WordCount([first_path, second_path])
    assert cmd.execute({}, '') == '0 1 1{s}1 2 3{s}1 3 4'.format(s=os.linesep,
                                                                 path=third_path)


if __name__ == '__main__':
    test_external_command()