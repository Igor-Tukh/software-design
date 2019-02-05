from source.commands.assignment import Assignment
from source.commands.cat import Cat
from source.commands.echo import Echo

import os

from source.commands.exit import Exit
from source.commands.external_command import ExternalCommand
from source.commands.pwd import PWD
from source.commands.wc import WordCount


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
    assert cmd.execute({}, '123') is 1  # Not None, it is important. Example : echo 1 | exit
    cmd = Exit([])
    assert cmd.execute({}, None) is None


def test_external_command():
    cmd = ExternalCommand(['ls'])
    assert len(cmd.execute({}, '').split(os.linesep)) == 3


def test_pwd():
    cmd = PWD(['ls'])
    assert cmd.execute({}, 'a') == os.getcwd()  # it is bad check, bad the only one possible :)


def test_wc():
    path = os.path.join(os.getcwd(), 'hw01-CLI', 'tests', 'resources', '3.txt')
    cmd = WordCount([os.path.join(os.getcwd(), 'hw01-CLI', 'tests', 'resources', '1.txt'),
                     os.path.join(os.getcwd(), 'hw01-CLI', 'tests', 'resources', '2.txt'),
                     path])
    print(cmd.execute({}, ''))
    assert cmd.execute({}, '') == '1 1 1{s}2 2 3{s}wc: \'{path}\': No such file{s}3 3 4'.format(s=os.linesep,
                                                                                                path=path)


if __name__ == '__main__':
    test_exit()
    test_external_command()
