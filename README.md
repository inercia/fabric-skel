Description
===========

A Fabric skeleton for managing deployments, starting/stopping services, qa, etc...

Building
========

Before building the software, you will need the Python 'virtualenv' package.

Then you can build the software with

    $ make

This will create a virtual environment and download Fabric for you.

Configuring the system
======================

In order to properly configure the system, you must search for all the occurrences
of the string XXXXX and replace them with the appropriate values.

Then you must check the configuration file, `manager.py`, and set the right
parameters. It is specially important to define the _roles_ and the _machines_ that
belong to each role...

Running the manager
===================

Once the virtual environment is ready, you can checkout the list of tasks available
with:

    $ ./manager.py

Some of our predefined tasks are:

    control.restart            Restart the service
    control.restart_i          Restart the service (interactive)
    control.start              Start the service
    control.start_i            Start the service (interactive)
    control.stop               Stop the service
    control.stop_i             Stop the service (interactive)
    control.machine.halt       Shutdown the machine [param: delay=now (seconds)]
    control.machine.halt_i     Shutdown the machine [param: delay=now (seconds)] (interactive)
    control.machine.restart    Restart the machine [param: delay=now (seconds)]
    control.machine.restart_i  Restart the machine [param: delay=now (seconds)]  (interactive)
    control.proc.kill          Kill a process id [params: pid=?, signum=6]
    control.proc.killall       Kill all processes with some name [params: name=?, signum=6]
    deploy                     Deploy the packages in the QA machines
    deploy.deploy              Deploy the packages in the QA machines
    ...

You can run a specific task by invoking the program with:

    $ ./manager.py <TASK>

This will run the task `TASK` in all the machines defined in the config file. But
you can run the task in group of machines by appending a `role=` argument. For example:

    $ ./manager.py dump.os_environ:role=production

will dump the OS environment variables only in production machines.




