#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#


import os

from fabric.api                 import env, task, serial, roles
from fabric.api                 import execute

from fabric.colors              import red, green, yellow
from fabric.contrib.console     import confirm


@task
@roles('testing', 'production')
def run (topdir = None):
    """
    Deploy the packages in the production machines
    """
    if not topdir:
        topdir= os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    print(green("Installing packages at %s" % str(env.host_string)))

    from jenkins import download
    execute(download)

    packages_dir = os.path.join(topdir, 'packages')

    from utils import install_packages_in
    install_packages_in(env, packages_dir, env.packages.debs.splitlines())

    print(red("... XXXXX should be restarted at %s!" % env.host_string))

@task
@serial
@roles('testing', 'production')
def run_i ():
    """
    Deploy the packages in the production machines (interactive)
    """
    if confirm(red('Install the packages at the %s?' % (env.host_string)), default = False):
        execute(run)
