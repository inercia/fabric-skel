#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#


import sys

from fabric.api                 import env, parallel, serial, roles, run
from fabric.api                 import execute
from fabric.context_managers    import settings
from fabric.operations          import sudo

from fabric.colors              import red, green, yellow
from fabric.contrib.console     import confirm
from fabric.contrib.files       import exists

from ..utils                    import run_bg, sudo_bg
from ..utils                    import manager_task


import machine
import proc




####################################################################################################


INITD_SCRIPT = '/etc/init.d/XXXX'

def _service(command, background = True):
    if not exists(INITD_SCRIPT):
        print(red('script %s not found' % INITD_SCRIPT))
        sys.exit(1)

    full_command = "%s %s" % (INITD_SCRIPT, command)

    with settings(warn_only = True):
        if background:
            sudo_bg(full_command)
        else:
            sudo(full_command)



####################################################################################################


@manager_task
@parallel
@roles('testing', 'production')
def start(background = True):
    """
    Start the service
    """
    print(green('Starting service at %s' % (env.host_string)))
    _service('start', background = background)

@manager_task
@serial
@roles('testing', 'production')
def start_i(background = True):
    """
    Start the service (interactive)
    """
    if confirm(red('Start service at %s?' % (env.host_string)), default = False):
        execute(start, background = background)

@manager_task
@parallel
@roles('testing', 'production')
def restart(background = True):
    """
    Restart the service
    """
    print(green('Restarting service at %s' % (env.host_string)))
    _service('restart', background = background)

@manager_task
@serial
@roles('testing', 'production')
def restart_i(background = True):
    """
    Restart the service (interactive)
    """
    if confirm(red('Restart service at %s?' % (env.host_string)), default = False):
        execute(restart, background = background)

@manager_task
@parallel
@roles('testing', 'production')
def stop(background = True):
    """
    Stop the service
    """
    print(green('Stoping service at %s' % (env.host_string)))
    _service('stop', background = background)

@manager_task
@serial
@roles('testing', 'production')
def stop_i(background = True):
    """
    Stop the service (interactive)
    """
    if confirm(red('Stop service at %s?' % (env.host_string)), default = False):
        execute(stop, background = background)
