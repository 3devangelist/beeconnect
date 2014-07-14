#!/usr/bin/env python
"""beetf

Usage:
beetf [-i -v=<idVendor> -p=<idProduct> --in=<epIn> --out=<epOut>] <>
beetf (-h | --help | --version)

Options:
    --version           Show version.
    -h, --help          Show this screen and exit.
    -i, --interactive   Interactive Mode 
    -v=<idVendor>       Vendor id  [default: 0xffff].
    -p=<idProduct>      Product id [default: 0x014e].
    --in=<epIn>         End point "in" in hex [default: 82].
    --out=<epOut>       End point "out" in hex [default: 05].

"""
from __future__ import unicode_literals, print_function
from docopt import docopt, DocoptExit
import sys
import cmd
import usb.core
import usb.util

__version__ = "0.1.0"
__author__ = "Rui Teixeira"
__license__ = "MIT"


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    print('test')
    def fn(self, arg):

        #test for a system command
        if('!' in arg):
            print('Fix: shell command not working')
            return

        print(dispatch(arg))
        
        print('!!!!')
        #check for a terminal, if not send to device 
        if('-' not in arg[0]):
            print(dispatch(arg))
            return
        

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


class BeetfTerm (cmd.Cmd):
    
    intro = '\nWelcome (type -help for a list of commands.)\n'
    prompt = '(beetf) '
    file = None



    @docopt_cmd
    def do_test(self, arg):
        """Usage: <arg>... 
        """
        print(arg)


    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

    def do_EOF(self, line):
        print('Good Bye!')
        exit()

#####
opt = docopt(__doc__, sys.argv[1:])

#Device starts Null
dev = None

def dispatch(msg):

    #Check for the device
    if dev is None:
        return -1    
    
    print(msg)

    out_ep = int(opt['--out'], 16)
    in_ep = int(opt['--in'], 16)
    
    #Send message 
    msg_len = dev.write(out_ep, msg, 100)
    print(msg_len)

    if(msg_len != len(msg)):
        print("ToDo: some error testing ")

    #Read reponse
    ret = dev.read(in_ep, 512, 100)
    print(ret)
    sret = ''.join([chr(x) for x in ret])

    print(sret)
    return sret
    
def initialize_usb():
    v = int(opt['-v'], 16)
    p = int(opt['-p'], 16)
    dev = usb.core.find(idVendor=v, idProduct=p)
     
    if dev is None:
        return None    
    dev.set_configuration()
    
    return dev

#for now it's all usb
dev = initialize_usb()
if dev is None:
    print("Device {}:{} not found".format(opt['-v'], opt['-p']))
    exit()


print(dispatch("m300"))
BeetfTerm().cmdloop()

print(opt)




