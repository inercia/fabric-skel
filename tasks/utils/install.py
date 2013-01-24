#
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#

import os
import sys
import fnmatch

from fabric.context_managers    import settings
from fabric.api                 import run
from fabric.api                 import put
from fabric.context_managers    import cd
from fabric.operations          import sudo
from fabric.colors              import red, green, yellow

from fabric.contrib.files       import exists


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




def install_packages_in(env, directory, patterns,
                        remote_upload_dir = '/tmp/'):
    """
    Install all the packages in the `directory` that match `pattern` in a remote machine.
    """
    SUBDIR = 'inst'

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
        
    print(green("... the following packages will be installed"))
    print(green("...... %s" % ', '.join(matches)))
    
    with cd(remote_upload_dir):
        print(yellow("... cleaning up old packages"))
        if exists(SUBDIR): run('rm -rf {subdir}'.format(subdir = SUBDIR))
        run('mkdir {subdir}'.format(subdir = SUBDIR))

    with cd(os.path.join(remote_upload_dir, SUBDIR)):
        print(yellow("... uploading packages"))
        for f in matches:
            put(f, '.')

        print(yellow("... installing software"))
        sudo('dpkg --install  *.deb')



def install_package_in(env, deb, remote_upload_dir = '/tmp/'):
    """
    Install all the packages in the `directory` that match `pattern` in a remote machine.
    """
    SUBDIR = 'inst'

    if os.path.exists(deb):
        print(red("%s packages not found"))
        return

    print(green("... the following packages will be installed"))
    print(green("...... %s" % deb))

    with cd(remote_upload_dir):
        print(yellow("... cleaning up old packages"))
        if exists(SUBDIR): run('rm -rf {subdir}'.format(subdir = SUBDIR))
        run('mkdir {subdir}'.format(subdir = SUBDIR))

    with cd(os.path.join(remote_upload_dir, SUBDIR)):
        print(yellow("... uploading packages"))
        put(deb, '.')

        print(yellow("... installing software"))
        sudo('dpkg --install  *.deb')




