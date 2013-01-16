#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#

import pprint

from fabric.api                 import run, env, task, roles, runs_once
from fabric.context_managers    import settings

from fabric.colors              import red, green, yellow



#
# auxiliary tasks
#

@task
@roles('testing', 'production')
def os_environ ():
    """
    Dump the OS environment variables on all machines
    """
    with settings(warn_only = True):
        run('export')

@task
@runs_once
def machines_roles ():
    """
    Dumps the current roles list
    """
    roledefs_str = pprint.pformat(env.roledefs, indent = 2)
    print(green("Currently defined roles:\n%s" % roledefs_str))

@task
@runs_once
def environ ():
    """
    Dumps the current Fabric environment
    """
    env_str = pprint.pformat(env, indent = 2)
    print(green("Currently defined environment:\n%s" % env_str))

@task
@runs_once
def machines ():
    """
    Dumps the current machines list with their variables
    """
    machines_str = pprint.pformat(env.machines, indent = 2)
    print(green("Currently defined machines:\n%s" % machines_str))


