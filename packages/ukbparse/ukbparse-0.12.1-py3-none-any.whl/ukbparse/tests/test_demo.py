#!/usr/bin/env python
#
# test_demo.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import time
import os.path as op
import multiprocessing as mp

from unittest import mock

import notebook.notebookapp as notebookapp
import ukbparse.scripts.demo as ukbdemo


def test_demo():

    def shutdown():
        time.sleep(3)
        for server in notebookapp.list_running_servers():
            notebookapp.shutdown_server(server)

    mp.Process(target=shutdown).start()

    # add some extra args for running within docker
    if op.exists('/.dockerenv'): args = ['--allow-root', '--ip=0.0.0.0']
    else:                        args = None

    with mock.patch('sys.argv', ['ukbparse_demo']):
        ukbdemo.main(args)
