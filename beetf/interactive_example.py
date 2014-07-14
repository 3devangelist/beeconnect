#!/usr/bin/env python
"""beetf

Usage:
beetf usb [--v=<idVendor> --p=<idProduct>]
beetf serial <port> [--baud=<n>] [--timeout=<seconds>]
beetf (-i | --interactive)
beetf (-h | --help | --version)

Options:
    -h --help       Show this screen.
    --version       Show version.
    -v=<idVendor>   Vendor id  [default: ffff].
    -p=<idProduct>  Product id [default: 014e].
    -i, --interactive  Interactive Mode
    -h, --help      Show this screen and exit.
    --baud=<n>      Baudrate [default: 9600]



"""
import cmd
import sys
from __future__ import unicode_literals, print_function
from docopt import docopt, DocoptExit

__version__ = "0.1.0"
__author__ = "Rui Teixeira"
__license__ = "MIT"



"""
"""

import sys
import cmd
from docopt import docopt, DocoptExit


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):
    intro = 'Welcome to my interactive program!' \
        + ' (type help for a list of commands.)'
    prompt = '(my_program) '
    file = None

    @docopt_cmd
    def do_tcp(self, arg):
        """Usage: tcp <host> <port> [--timeout=<seconds>]"""

        print(arg)

    @docopt_cmd
    def do_serial(self, arg):
        """Usage: serial <port> [--baud=<n>] [--timeout=<seconds>]
Options:
    --baud=<n>  Baudrate [default: 9600]
        """

        print(arg)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)
