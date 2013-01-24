#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#



import os

from fabric.api                 import run, env, serial, roles
from fabric.context_managers    import cd, settings
from fabric.colors              import red, green, yellow

from ..utils                    import manager_task


#
# logs
#

def _tailf(filename):
    print(green('%s at %s' % (filename, env.host_string)))
    with settings(warn_only = True):
        run('[ -f {f} ] && tail {f} || echo "file not found"'.format(f = filename))


####################################################################################################

@manager_task
@serial
@roles('testing', 'production')
def syslog():
    """
    Prints the tail of /var/log/syslog
    """
    _tailf('/var/log/syslog')

@manager_task
@serial
@roles('testing', 'production')
def kern():
    """
    Prints the tail of /var/log/kern.log
    """
    _tailf('/var/log/kern.log')

@manager_task
@serial
@roles('testing', 'production')
def dmesg():
    """
    Prints the tail of /var/log/dmesg
    """
    _tailf('/var/log/dmesg')

@manager_task
@serial
@roles('testing', 'production')
def boot():
    """
    Prints the tail of /var/log/boot
    """
    _tailf('/var/log/boot')

@manager_task
@serial
@roles('testing', 'production')
def dpkg():
    """
    Prints the tail of /var/log/dpkg.log
    """
    _tailf('/var/log/dpkg.log')
