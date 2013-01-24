#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#


from fabric.api                 import env, parallel, serial, roles, execute
from fabric.operations          import sudo

from fabric.colors              import red, green, yellow
from fabric.contrib.console     import confirm

from ..utils                    import manager_task


@manager_task
@roles('testing', 'testing-aps', 'production')
def halt(delay = None):
    """
    Shutdown the machine [param: delay=now (seconds)]
    """
    if not delay:
        sudo('shutdown -h now')
    else:
        assert isinstance(delay, (int, long))
        assert delay >= 60
        minutes = (delay / 60)
        sudo('shutdown -h +%d' % minutes)

@manager_task
@roles('testing', 'testing-aps', 'production')
def halt_i(delay = None):
    """
    Shutdown the machine [param: delay=now (seconds)] (interactive)
    """
    if confirm(red('Shutdown the machine %s?' % (env.host_string)), default = False):
        execute(halt, delay = delay)


@manager_task
@roles('testing', 'testing-aps', 'production')
def restart(delay = None):
    """
    Restart the machine [param: delay=now (seconds)]
    """
    if not delay:
        sudo('shutdown -r now')
    else:
        assert isinstance(delay, (int, long))
        assert delay >= 60
        minutes = (delay / 60)
        sudo('shutdown -r +%d' % minutes)


@manager_task
@roles('testing', 'testing-aps', 'production')
def restart_i(delay = None):
    """
    Restart the machine [param: delay=now (seconds)]  (interactive)
    """
    if confirm(red('Restart the machine %s?' % (env.host_string)), default = False):
        execute(restart, delay = delay)
