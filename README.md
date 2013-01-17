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

Our predefined tasks are:

	config.upload        Upload a list of files (separated by ':') [params: orig=?, dest=/etc/]
	config.upload_XXXXX  Upload the XXXXX.conf file (after doing replacements)
	control.restart      Restart the XXXXX systems
	control.restart_i    Restart the XXXXX systems (interactive)
	control.start        Start the XXXXX systems
	control.start_i      Start the XXXXX systems (interactive)
	control.stop         Stop the XXXXX systems
	control.stop_i       Stop the XXXXX systems (interactive)
	deploy.run           Deploy the packages in the production machines
	deploy.run_i         Deploy the packages in the production machines (interactive)
	dump.environ         Dumps the current Fabric environment
	dump.machines        Dumps the current machines list with their variables
	dump.machines_roles  Dumps the current roles list
	dump.os_environ      Dump the OS environment variables on all machines
	jenkins.download     Get the latests package versions from Jenkins
	logs.cleanup         Cleanup all the logs
	logs.tail            Prints the tail of PREFIX/logs/XXXXX.log
	qa.deploy            Deploy the packages in the QA machines
	qa.run               Deploy the packages in the QA machines, and launch the testing tool
	qa.run_tests         Run the tester in the QA machines

You can run a specific task by invoking the program with:

    $ ./manager.py <TASK>

This will run the task `TASK` in all the machines defined in the config file. But
you can run the task in group of machines by appending a `role=` argument. For example:

    $ ./manager.py dump.os_environ:role=production

will dump the OS environment variables only in production machines.




