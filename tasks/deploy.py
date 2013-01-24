#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#


import os

from fabric.api                 import env, serial, roles
from fabric.api                 import execute

from fabric.colors              import red, green, yellow
from fabric.contrib.console     import confirm

from utils                      import manager_task


def _deploy_multiple(topdir = None):
    if not topdir:
        topdir= os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    print(green("Installing packages at %s" % str(env.host_string)))

    from jenkins import download
    execute(download)

    packages_dir = os.path.join(topdir, 'packages')

    from utils.install import install_packages_in
    install_packages_in(env, packages_dir, env.packages.debs.splitlines())

    print(red("... service should be restarted at %s!" % env.host_string))


def _deploy_one(deb):
    print(green("Installing packages at %s" % str(env.host_string)))

    from utils.install import install_package_in
    install_package_in(env, deb)

####################################################################################################

@manager_task(default = True)
@roles('testing', 'production')
def jenkins (topdir = None):
    """
    Deploy the packages from Jenkins in the production machines
    """
    _deploy_multiple(topdir)

@manager_task
@serial
@roles('testing', 'production')
def jenkins_i ():
    """
    Deploy the packages from Jenkins in the production machines (interactive)
    """
    if confirm(red('Install the packages at the %s?' % (env.host_string)), default = False):
        execute(jenkins)



@manager_task()
@roles('testing', 'production')
def deb (deb):
    """
    Deploy a Debian package in the production machines [params: deb=?]
    """
    _deploy_one(deb)
