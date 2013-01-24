#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#


from fabric.api                 import roles, serial, sudo

from ..utils                    import manager_task



NMCLI_EXE = '/usr/bin/nmcli'


#
# NetworkManager tasks
#

@manager_task
@serial
@roles('testing',  'production')
def up(con):
    """
    Bring a NetworkManager connection up [params: con=?]
    """
    sudo('%s con up id "%s"' % (NMCLI_EXE , con))

@manager_task
@serial
@roles('testing',  'production')
def down(con):
    """
    Bring a NetworkManager connection down [params: con=?]
    """
    sudo('%s con down id "%s"' % (NMCLI_EXE , con))

@manager_task
@serial
@roles('testing',  'production')
def ls():
    """
    List the NetworkManager connections
    """
    sudo('%s con' % (NMCLI_EXE))
