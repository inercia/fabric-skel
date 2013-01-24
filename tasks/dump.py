#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#

import pprint

from fabric.api                 import run, env, roles, runs_once, serial
from fabric.context_managers    import settings

from fabric.colors              import red, green, yellow

from utils                      import manager_task
from utils                      import ping as do_ping



#
# auxiliary tasks
#

@manager_task
@roles( 'testing', 'production')
def os_environ ():
    """
    Dump the OS environment variables on all machines
    """
    with settings(warn_only = True):
        run('export')

@manager_task
@runs_once
def machines_roles ():
    """
    Dumps the current roles list
    """
    roledefs_str = pprint.pformat(env.roledefs, indent = 2)
    print(green("Currently defined roles:\n%s" % roledefs_str))

@manager_task
@runs_once
def environ ():
    """
    Dumps the current Fabric environment
    """
    env_str = pprint.pformat(env, indent = 2)
    print(green("Currently defined environment:\n%s" % env_str))

@manager_task
@runs_once
def machines ():
    """
    Dumps the current machines list with their variables
    """
    machines_str = pprint.pformat(env.machines, indent = 2)
    print(green("Currently defined machines:\n%s" % machines_str))



@manager_task
@serial
@roles('testing', 'production')
def ping():
    """
    Print an echo in the machine
    """
    if do_ping():
        print(green("%s is alive" % env.host_string))
    else:
        print(red("%s does not respond" % env.host_string))

@manager_task
@serial
@roles('testing', 'production')
def uptime():
    """
    Print the time up and load averages ("uptime")
    """
    run('uptime')

@manager_task
@serial
@roles('testing',  'production')
def mounts():
    """
    Print the mounted devices ("mount")
    """
    run('mount')

@manager_task
@serial
@roles('testing', 'production')
def df():
    """
    Print the available space in devices ("df -h")
    """
    run('df -h')

@manager_task
@serial
@roles('testing', 'production')
def ps():
    """
    Print the processes ("ps axf")
    """
    run('ps axf')
