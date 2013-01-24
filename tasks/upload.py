#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#

import os
import sys
import glob

from fabric.api                 import env, serial, roles
from fabric.contrib.files       import upload_template

from fabric.colors              import red, green, yellow
from fabric.contrib.console     import confirm

from utils                      import manager_task


@manager_task(default = True)
@serial
@roles('testing', 'production')
def files_i(orig = None, dest = '/etc/'):
    """
    Upload a list of files (separated by ':') [params: orig=?, dest=/etc/] (interactive)
    """
    if not orig:
        print(red('no local file provided'))
        sys.exit(1)

    try:                context = env.contexts[env.host_string]
    except IndexError:  context = {}

    patterns_list = orig.split(':')

    orig_list = []
    for pattern in patterns_list:
        for filename in glob.glob(pattern):
            full_filename = os.path.abspath(filename)
            orig_list.append(full_filename)

    if confirm(red('Upload %d files to %s:%s?' % (len(orig_list), env.host_string, dest)), default = False):
        for f in orig_list:
            if not os.path.exists(f):
                print(red('... %s does not exist! -> skipping' % f))
                continue

            print(green('... uploading %s' % (f)))

            upload_template(f, dest,
                            context             = context,
                            use_jinja           = False,
                            use_sudo            = True,
                            backup              = True)


@manager_task
@serial
@roles('testing', 'production')
def directory_i(orig = None, dest = None):
    """
    Upload a directory contents [params: orig=?, dest=?] (interactive)
    """
    if not orig:
        print(red('no local directory provided'))
        sys.exit(1)

    if not dest:
        print(red('no remote directory provided'))
        sys.exit(1)

    try:                context = env.contexts[env.host_string]
    except IndexError:  context = {}

    if confirm(red('Upload everything from %s to %s:%s?' % (orig, env.host_string, dest)), default = False):
        for root, dirs, files in os.walk(orig):
            for x in files:
                f = os.path.join(root, x)
                print(green('... uploading %s' % (f)))
                upload_template(f, dest,
                                context             = context,
                                use_jinja           = False,
                                use_sudo            = True,
                                backup              = True)


