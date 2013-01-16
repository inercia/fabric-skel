#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#


from fabric.api                 import env, task, parallel, serial, roles
from fabric.api                 import execute
from fabric.context_managers    import settings
from fabric.operations          import sudo

from fabric.colors              import red, green, yellow
from fabric.contrib.console     import confirm


@task
@parallel
@roles('testing', 'production')
def start():
    """
    Start the XXXXX systems
    """
    print(green('Starting XXXXX at %s' % (env.host_string)))
    with settings(warn_only = True):
        sudo('rm -f nohup*')
        sudo('[ -f /etc/init.d/XXXXX ] && nohup /etc/init.d/XXXXX start || echo "No service script found!!"')

@task
@serial
@roles('testing', 'production')
def start_i():
    """
    Start the XXXXX systems (interactive)
    """
    if confirm(red('Start XXXXX at %s?' % (env.host_string)), default = False):
        execute(start)

@task
@parallel
@roles('testing', 'production')
def restart():
    """
    Restart the XXXXX systems
    """
    print(green('Restarting XXXXX at %s' % (env.host_string)))
    with settings(warn_only = True):
        sudo('rm -f nohup*')
        sudo('[ -f /etc/init.d/XXXXX ] && nohup /etc/init.d/XXXXX restart || echo "No service script found!!"')

@task
@serial
@roles('testing', 'production')
def restart_i():
    """
    Restart the XXXXX systems (interactive)
    """
    if confirm(red('Restart XXXXX at %s?' % (env.host_string)), default = False):
        execute(restart)

@task
@parallel
@roles('testing', 'production')
def stop():
    """
    Stop the XXXXX systems
    """
    print(green('Stoping XXXXX at %s' % (env.host_string)))
    with settings(warn_only = True):
        sudo('rm -f nohup*')
        sudo('[ -f /etc/init.d/XXXXX ] && nohup /etc/init.d/XXXXX stop || echo "No service script found!!"')

@task
@serial
@roles('testing', 'production')
def stop_i():
    """
    Stop the XXXXX systems (interactive)
    """
    if confirm(red('Stop XXXXX at %s?' % (env.host_string)), default = False):
        execute(stop)
