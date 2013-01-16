#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#


import os

from fabric.api                 import run, env, task, parallel, roles
from fabric.context_managers    import cd, settings
from fabric.operations          import sudo
from fabric.colors              import red, green, yellow



#
# logs
#

@task
@roles('testing', 'production')
def tail():
    """
    Prints the tail of PREFIX/logs/XXXXX.log
    """
    f = os.path.join(env.admin.prefix, 'logs', 'XXXXX.log')
    print(green('%s at %s' % (f, env.host_string)))
    with settings(warn_only = True):
        run('[ -f {f} ] && tail {f} || echo "file not found"'.format(f = f))

@task
@parallel
@roles('testing', 'production')
def cleanup ():
    """
    Cleanup all the logs
    """
    with cd(env.admin.prefix):
        with settings(warn_only = True):
            sudo('[ -d logs ] && rm -rf logs/*')

