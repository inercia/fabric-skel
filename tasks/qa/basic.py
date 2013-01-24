#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#

import time

from fabric.api                 import run, env, parallel, roles, runs_once, serial
from fabric.api                 import execute
from fabric.colors              import red, green, yellow

from ..utils                    import manager_task





#: time to wait after restarting the packages
AFTER_INSTALL_DELAY=30


#
# Basic QA
#

@manager_task(default = True)
@runs_once
def start(runtime = None, desc = None, url = None):
    """
    Perform a basic QA workflow [params: runtime=(from cfg), desc=None, url=None]
    """
    pass
