#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#

from fabric.api                 import run, env, parallel, roles, runs_once, serial
from fabric.colors              import red, green, yellow

from ..utils                    import manager_task


#
# QA
#

@manager_task
@parallel
@roles('testing')
def deploy ():
    """
    Deploy the packages in the QA machines
    """
    print(green("Installing packages at %s" % str(env.host_string)))
    from ..deploy import _deploy_multiple
    _deploy_multiple()

