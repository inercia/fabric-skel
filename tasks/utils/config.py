#
# Authors: Alvaro Saurin <saurin@tid.es> - 2013
#
#

import os
import sys

from fabric.utils               import _AttributeDict


#: default Fabric configuration file
FABRIC_CFG = 'manager.cfg'


try:
    from configparser           import ConfigParser, ExtendedInterpolation
except ImportError:
    print "ERROR: configparser is not installed"
    sys.exit(1)



###################################################################################################


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


    def from_section(cfg, section):
        d = {}
        for option in cfg.options(section):
            option = str(option)
            value = str(cfg.get(section, option))

            ## check if this is a boolean
            if value.lower() in ['true', 'false']:
                d[option] = True if value.lower() == 'true' else False
            else:
                try:                            ## try to detect if it is an integer
                    d[option] = int(value)
                except ValueError:
                    d[option] = value

        return d

    # load the roles, machines and contexts (for templates substitutions)
    roledefs = {}
    machines = {}
    contexts = {}

    for section in [x for x in cfg.sections() if x.lower().startswith('role|')]:
        role_name = str(section.lower().replace('role|', '').strip())
        if not role_name in env.roledefs:
            roledefs[role_name] = []

        for host in cfg.options(section):

            host = str(host).lower()

            ## append all the machines defined in the roles...
            if not host in roledefs[role_name]:
                roledefs[role_name].append(host)

            ## check if there is a [host|MACHINE]
            machine_section = 'host|' + host
            if cfg.has_section(machine_section):
                if host in machines:
                    machines[host].update(from_section(cfg, machine_section))
                else:
                    machines[host] = from_section(cfg, machine_section)

            ## check if there is a [templates|MACHINE]
            templates_section = 'templates|' + host
            if cfg.has_section(templates_section):
                if host in contexts:
                    contexts[host].update(from_section(cfg, templates_section))
                else:
                    contexts[host] = from_section(cfg, templates_section)

    env.roledefs = roledefs
    env.machines = machines
    env.contexts = contexts

    ## treat the 'auth' section (if present)
    if cfg.has_section('auth'):
        try:
            env.key_filename = [os.path.abspath(x) for x in  str(cfg.get('auth', 'certs')).splitlines()]
        except KeyError:
            print 'WARNING: no certificates directory specified in config file...'

        try:
            env.user = str(cfg.get('auth', 'user'))
        except KeyError:
            print 'WARNING: no default username specified in config file...'

        try:
            env.password = str(cfg.get('auth', 'password'))
        except KeyError:
            print 'WARNING: no default password specified in config file...'

    # the environment sections
    for section in [x for x in cfg.sections() if x.lower().startswith('env|')]:
        env_name = str(section.replace('env|', '').strip())

        if env_name == 'global':
            env.update(_AttributeDict(from_section(cfg, section)))
        else:
            if not env_name in env:
                d = from_section(cfg, section)
                env[env_name] = _AttributeDict(d)

    ## and some defaults...

    ## do not use the local SSH config files...
    env.no_agent = True
    env.no_keys = True
    env.disable_known_hosts = True
