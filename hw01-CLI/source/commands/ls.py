import os
import pathlib

from source.commands.command import Command


def get_list_of_files(sub_dir):
    return '\n'.join([str(x.name) for x in pathlib.Path(os.path.join(os.getcwd(), sub_dir)).iterdir()])


class Ls(Command):
    """
    ls command, print content of current directory
    """

    def execute(self, variables_environment, previous_output):
        return get_list_of_files('./') if len(self.args) == 0 else get_list_of_files(self.args[0])
