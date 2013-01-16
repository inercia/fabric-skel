Description
===========

A Fabric skeleton for managing deployments, starting/stopping services, qa, etc...

Building
========

Before building the software, you will need the Python 'virtualenv' package.

Then you can build the software with

    $ make
    
Running the manager
===================

Checkout the list of tasks available with

    $ ./manager.py

You can also check the configuration file we are currently using in `manager.cfg`.

You can run a specific task by invoking the program with:

    $ ./manager.py <TASK>

This will run the task `TASK` in all the machines defined in the config file. But
you can run the task in group of machines with the `-R` argument, and there are two
machines groups defined so far: production and testing.



