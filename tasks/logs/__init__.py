#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#


from fabric.api                 import run, env, serial, roles
from fabric.context_managers    import cd, settings
from fabric.operations          import sudo

from ..utils                    import manager_task

import tail


#
# logs
#

@manager_task
@serial
@roles('testing', 'production')
def cleanup ():
    """
    Cleanup all the logs
    """
    with cd(env.installation.prefix):
        with settings(warn_only = True):
            sudo('[ -d logs ] && rm -rf logs/*')

@manager_task
@serial
@roles('testing', 'production')
def ls():
    """
    List all the installation logs
    """
    with cd(env.installation.logs_dir):
        with settings(warn_only = True):
            run('ls')

