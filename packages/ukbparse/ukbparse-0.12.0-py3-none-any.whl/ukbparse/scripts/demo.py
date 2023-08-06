#!/usr/bin/env python
#
# demo.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import sys
import os.path as op

import jupyter_core.command as jupyter_command

def main():

    thisdir = op.abspath(op.dirname(__file__))
    nbdir = op.join(thisdir, 'demo')

    sys.argv[1:] = ['notebook', '--notebook-dir', nbdir]

    sys.exit(jupyter_command.main())


if __name__ == '__main__':
    main()
