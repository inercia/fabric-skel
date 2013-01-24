#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#



import os
import fnmatch
import urllib
import tempfile
import zipfile
import shutil

from fabric.api                 import env, roles, runs_once, serial
from fabric.colors              import red, green, yellow

from utils                      import manager_task


@manager_task
@runs_once
@serial
def download (topdir = None):
    """
    Get the latests package versions from Jenkins
    """
    if not topdir:
        topdir= os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    packages_dir = os.path.join(topdir, 'packages')

    print(green("Gathering packages from %s to %s" % (str(env.jenkins.host), packages_dir)))

    try:
        if os.path.exists(packages_dir):
            shutil.rmtree(packages_dir)
    except:
        pass

    try:
        if not os.path.exists(packages_dir):
            os.mkdir(packages_dir)
    except OSError:
        pass

    dirpath = tempfile.mkdtemp()
    zip_file = os.path.join(dirpath, 'zip_file')

    for artifact in env.jenkins.artifacts.splitlines():
        print(yellow("... downloading %s" % str(artifact)))
        urllib.urlretrieve (artifact, zip_file)

        print(yellow("...... extracting Zip file"))
        with zipfile.ZipFile(zip_file, 'r') as artifact_zip:
            artifact_zip.extractall(dirpath)

    matches = []
    for root, dirnames, filenames in os.walk(dirpath):
        for filename in fnmatch.filter(filenames, '*.deb'):
            full_filename = os.path.join(root, filename)
            matches.append(full_filename)
            shutil.copy(full_filename, packages_dir)

    print(yellow("... packages obtained:"))
    for p in matches:
        print(yellow("...... %s" % str(p)))

    shutil.rmtree(dirpath)

    print(green("... files stored at %s" % str(packages_dir)))
