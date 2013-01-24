#!/usr/bin/python
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#


from fabric.api                 import roles
from fabric.operations          import sudo

from ..utils                    import manager_task


@manager_task
@roles('testing', 'production')
def kill(pid, signum = 6):
    """
    Kill a process id [params: pid=?, signum=6]
    """
    sudo('kill -%d %d' % (signum, pid))

@manager_task
@roles('testing', 'production')
def killall(name, signum = 6):
    """
    Kill all processes with some name [params: name=?, signum=6]
    """
    sudo('killall -%d %s' % (signum, name))
