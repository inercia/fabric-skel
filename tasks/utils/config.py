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



def load_cfg(env, root):
    """
    custom configuration system

    :param env: the environment
    """

    if 'FABRIC_CFG' in os.environ:
        filename = os.environ['FABRIC_CFG']
    else:
        filename = os.path.abspath(os.path.join(root, FABRIC_CFG))
    if not os.path.exists(filename):
        print 'ERROR: Fabric configuration file "%s" not found' % filename
        print 'ERROR: you must use a %s file' % FABRIC_CFG
        print 'ERROR: (or specify the file name on the FABRIC_CFG environment variable)'
        sys.exit(1)

    ## load the configuration file
    cfg = ConfigParser(default_section = 'defaults', interpolation = ExtendedInterpolation())
    try:
        with open(filename, 'r') as cfg_file:
            cfg.read_string(unicode(cfg_file.read()))
    except Exception, e:
        print "ERROR: reading %s:" % filename, str(e).lower()
        sys.exit(1)

    # load the roles and machines
    roledefs = {}
    machinedefs = {}
    for section in [x for x in cfg.sections() if x.lower().startswith('role|')]:
        role_name = str(section.lower().replace('role|', '').strip())
        if not role_name in env.roledefs:
            roledefs[role_name] = []

        for host in cfg.options(section):
            machine_section = 'host|' + host
            if cfg.has_section(machine_section):
                machinedefs[str(host)] = {}
                roledefs[str(role_name)].append(str(host.lower()))
                for option in cfg.options(machine_section):
                    machinedefs[host][str(option.upper())] = str(cfg.get(machine_section, option))

    env.roledefs = roledefs
    env.machines = machinedefs

    # ... and the environment sections
    for section in [x for x in cfg.sections() if x.lower().startswith('env|')]:
        env_name = str(section.replace('env|', '').strip())
        if env_name == 'global':
            d = {}
            for option in cfg.options(section):
                d[str(option)] = str(cfg.get(section, option))
            env.update(_AttributeDict(d))
        elif env_name == 'auth':
            d = {}
            for option in cfg.options(section):
                d[str(option)] = str(cfg.get(section, option))

            ## do some specific treatment for some special keys...
            try:
                env.key_filename = [os.path.abspath(x) for x in d['certs'].splitlines()]
            except KeyError:
                print 'ERROR: no certificates directory specified in config file...'
                sys.exit(1)

            try:
                env.user = d['username']
            except KeyError:
                print 'WARNING: no default username specified in config file...'

            try:
                env.password = d['password']
            except KeyError:
                print 'WARNING: no default passworrd specified in config file...'

        else:
            if not env_name in env:
                d = {}
                for option in cfg.options(section):
                    d[str(option)] = str(cfg.get(section, option))
                env[env_name] = _AttributeDict(d)

    ## and some defaults...

    ## do not use the local SSH config files...
    env.no_agent = True
    env.no_keys = True
    env.disable_known_hosts = True

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




