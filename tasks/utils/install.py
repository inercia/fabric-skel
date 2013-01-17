#
# ClubWifi
# Copyright Telefonica I+D, 2013
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#

import os
import sys
import fnmatch

from fabric.utils               import _AttributeDict
from fabric.context_managers    import settings
from fabric.api                 import run
from fabric.api                 import put
from fabric.context_managers    import cd
from fabric.operations          import sudo
from fabric.colors              import red, green, yellow



#: default Fabric configuration file
FABRIC_CFG = 'manager.cfg'


try:
    from configparser           import ConfigParser, ExtendedInterpolation
except ImportError:
    print "ERROR: configparser is not installed"
    sys.exit(1)



###################################################################################################


# some aux functions...
def _exists(path):
    """
    check if a file exists on a remote host

    :param path:
    :return: True if it exists, False otherwise
    """
    with settings(warn_only = True):
        return bool(int(run('[ -e %s ] && echo 1 || echo 0' % path)))


def install_packages_in(env, directory, patterns):
    """
    Install all the packages in the `directory` that match `pattern` in a remote machine.
    """
    matches = set()
    for root, dirnames, filenames in os.walk(directory):
        for pattern in patterns:
            for filename in fnmatch.filter(filenames, pattern):
                full_filename = os.path.join(root, filename)
                matches.add(full_filename)
                break

    if len(matches) == 0:
        print(red("no packages to install in %s" % directory))
        return
        
    print(green("the following packages will be installed"))
    print(green("... %s" % ', '.join(matches)))
    
    print(yellow("cleaning up old packages"))    

    with cd(env.installation.prefix):
        print(yellow("... cleaning up old packages"))
        if not _exists('tmp'): run('mkdir tmp')
        run('rm -rf tmp/*')

    directory = os.path.join(env.installation.prefix, 'tmp')
    with cd(directory):
        print(yellow("... uploading packages"))
        for f in matches:
            put(f, '.')

        print(yellow("... installing software"))
        sudo('dpkg --install  *.deb')




