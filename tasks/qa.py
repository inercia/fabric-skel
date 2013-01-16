#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# XXXXX Service
# Copyright Telefonica I+D, 2013
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#


from fabric.api                 import run, env, task, parallel, roles
from fabric.api                 import execute
from fabric.colors              import red, green, yellow



#
# QA
#

@task
@parallel
@roles('testing')
def deploy ():
    """
    Deploy the packages in the QA machines
    """
    print(green("Installing packages at %s" % str(env.host_string)))
    from deploy import run as run_deploy
    execute(run_deploy)

@task
@parallel
@roles('testing')
def run_tests ():
    """
    Run the tester in the QA machines
    """
    print(green("Running %s at %s" % (str(env.stresser.script), str(env.host_string))))
    run(env.qa.script)


@task
def run(default = True):
    """
    Deploy the packages in the QA machines, and launch the testing tool
    """
    execute(deploy)
    execute(run_tests)

