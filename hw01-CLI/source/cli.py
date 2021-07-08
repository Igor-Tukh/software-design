import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from source.input_handler import InputHandler


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
    handler = InputHandler()

    while True:
        input_line = input()
        handler.process_input(input_line)
