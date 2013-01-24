#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#




from fabric.api                 import run, env, roles, runs_once, serial, sudo
from fabric.contrib.console     import confirm

from fabric.colors              import red, green, yellow

from ..utils                    import manager_task


import nm



#
# networking tasks
#

@manager_task
@serial
@roles('testing',  'production')
def hostname():
    """
    Print the hostname
    """
    run('hostname')

@manager_task
@serial
@roles('testing',  'production')
def ifconfig():
    """
    Print the devices table ("ifconfig")
    """
    run('/sbin/ifconfig')

@manager_task
@serial
@roles('testing',  'production')
def route():
    """
    Print the routes table ("route -n")
    """
    run('route -n')

@manager_task
@serial
@roles('testing',  'production')
def set_gateway_i(ip, dev = None):
    """
    Set the default gateway [params: ip=?, dev=None] (interactive)
    """
    command = 'route add default gw %s' % ip
    if dev:
        command += ' %s' % dev

    if confirm(red('Set the default geteway at %s to %s?' % (env.host_string, ip)), default = False):
        sudo(command)


@manager_task
@serial
@roles('testing',  'production')
def ifup(dev):
    """
    Bring up a device [params: dev=?]
    """
    sudo('ifup %s' % dev)

@manager_task
@serial
@roles('testing',  'production')
def ifdown(dev):
    """
    Bring down a device [params: dev=?]
    """
    sudo('ifdown %s' % dev)

