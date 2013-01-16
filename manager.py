#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#

from __future__ import with_statement
from __future__ import division

import os
import sys


# bootstrap variables
HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = HERE

FABRIC= os.path.join(PROJECT_ROOT, 'bin', 'fab')

PYTHON = os.path.abspath(os.path.join(PROJECT_ROOT, 'bin', 'python'))
FABUTILS_DIR = os.path.join(PROJECT_ROOT, '.')

help_str = """
Invoke one of these tasks with:

    $ {manager} <TASK_NAME>

and some tasks need some arguments. For example:

    $ {manager} config.upload:orig=img-utils/config/*

You can apply the task only in one machine with -H <MACHINE_NAME>, or on a group of
machines with -R <ROLE_NAME>. Checkout the machines/roles at the config file.
""".format(manager = __file__)

#  This is our entry point.
if __name__ == '__main__':
    import subprocess

    if not os.path.exists(FABRIC):
        print "'fabric' is missing. This software has not been properly installed..."
        sys.exit(0)
    
    if len(sys.argv) > 1:
        #  If we got an argument then invoke fabric with it.
        try:
            subprocess.call([FABRIC, '-f', os.path.abspath(__file__)] + sys.argv[1:])
        except KeyboardInterrupt:
            print
            print 'Interrupted... bye!'
        sys.exit(0)
    else:
        #  Otherwise list our targets.        
        subprocess.call([FABRIC, '-f', os.path.abspath(__file__), '--list'])
        print help_str
        print "Run \"%s --help\" for more details" % __file__
        sys.exit(0)


###################################################################################################

from fabric.api                 import env

## load the configuration file
sys.path.append(FABUTILS_DIR)
from tasks.utils import load_cfg, _exists
load_cfg(env, root = PROJECT_ROOT)

from tasks import *

