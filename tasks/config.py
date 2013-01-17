#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#

import os
import sys
import shutil
import glob

from fabric.api                 import env, task, serial, roles
from fabric.operations          import sudo
from fabric.contrib.files       import upload_template

from fabric.colors              import red, green, yellow
from fabric.contrib.console     import confirm




@task
@serial
@roles('testing', 'production')
def upload_XXXXX():
    """
    Upload the XXXXX.conf file (after doing replacements)
    """
    dest = os.path.join(env.installation.prefix, 'conf')

    try:                context = env.machines[env.host_string]
    except IndexError:  context = {}

    if confirm(red('Upload the new configuration files from %s at %s?' %
                   (env.templates.local_dir, env.host_string)),
               default = False):
        for f in env.templates.files:
            print(green('... uploading %s' % (f)))

            sudo('chown -R {user}:{group} {d}'.format(user    = env.installation.user,
                                                      group   = env.installation.group,
                                                      d       = env.installation.prefix))

            upload_template(f, dest,
                            context             = context,
                            use_jinja           = True,
                            template_dir        = env.templates.local_dir,
                            use_sudo            = False,
                            backup              = True)



@task
@serial
@roles('testing', 'production')
def upload(orig = None, remote = '/etc/'):
    """
    Upload a list of files (separated by ':') [params: orig=?, dest=/etc/]
    """
    if not orig:
        print(red('no local file provided'))
        sys.exit(1)

    try:                context = env.machines[env.host_string]
    except IndexError:  context = {}

    patterns_list = orig.split(':')

    orig_list = []
    for pattern in patterns_list:
        for filename in glob.glob(pattern):
            full_filename = os.path.abspath(filename)
            orig_list.append(full_filename)

    if confirm(red('Upload %d files to %s:%s?' % (len(orig_list), env.host_string, remote)), default = False):
        for f in orig_list:
            if not os.path.exists(f):
                print(red('... %s does not exist! -> skipping' % f))
                continue

            print(green('... uploading %s' % (f)))

            upload_template(f, remote,
                            context             = context,
                            use_jinja           = False,
                            use_sudo            = True,
                            backup              = True)


