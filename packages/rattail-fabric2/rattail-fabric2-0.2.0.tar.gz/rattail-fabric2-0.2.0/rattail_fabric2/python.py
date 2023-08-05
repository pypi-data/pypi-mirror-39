# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2018 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Fabric Library for Python
"""

from __future__ import unicode_literals, absolute_import

from contextlib import contextmanager

import six

from rattail_fabric2 import apt, exists, mkdir


def install_pip(c, use_apt=False, eager=True):
    """
    Install/upgrade the Pip installer for Python.
    """
    if use_apt:
        apt.install(c, 'python-pip')
    else:
        apt.install(c, 'build-essential', 'python-dev', 'libssl-dev', 'libffi-dev')
        if c.run('which pip', warn=True).failed:
            apt.install(c, 'python-pkg-resources', 'python-setuptools')
            c.sudo('easy_install pip')
            c.sudo('apt-get --assume-yes purge python-setuptools')
            pip(c, 'setuptools')
        pip(c, 'pip', upgrade=True)
        kwargs = {}
        if eager:
            kwargs['upgrade_strategy'] = 'eager'
        pip(c, 'setuptools', 'wheel', 'ndg-httpsclient', upgrade=True, **kwargs)


def pip(c, *packages, **kwargs):
    """
    Install one or more packages via ``pip install``.
    """
    upgrade = kwargs.pop('upgrade', False)
    upgrade = '--upgrade' if upgrade else ''
    upgrade_strategy = kwargs.pop('upgrade_strategy', None)
    if upgrade and upgrade_strategy:
        upgrade_strategy = '--upgrade-strategy {}'.format(upgrade_strategy)
    else:
        upgrade_strategy = ''
    use_sudo = kwargs.pop('use_sudo', True)
    runas_user = kwargs.pop('runas_user', None)
    if kwargs:
        raise RuntimeError("Unknown kwargs for pip(): {}".format(kwargs))
    packages = ["'{}'".format(p) for p in packages]
    cmd = 'pip install {} {} {}'.format(upgrade, upgrade_strategy, ' '.join(packages))
    if use_sudo:
        kw = {}
        if runas_user:
            kw['user'] = runas_user
        c.sudo(cmd, **kw)
    else:
        c.run(cmd)


def install_virtualenvwrapper(c, workon_home='/srv/envs', user='root', use_apt=False, configure_me=True):
    """
    Install the `virtualenvwrapper`_ system, with the given ``workon`` home,
    owned by the given user.
    """
    mkdir(c, workon_home, owner=user, use_sudo=True)
    if use_apt:
        apt.install(c, 'virtualenvwrapper')
    else:
        pip(c, 'virtualenvwrapper', upgrade=True)
        configure_virtualenvwrapper(c, user, workon_home)
        if configure_me:
            # TODO
            # configure_virtualenvwrapper(c, env.user, workon_home)
            raise NotImplementedError


def configure_virtualenvwrapper(c, user, workon_home='/srv/envs', wrapper='/usr/local/bin/virtualenvwrapper.sh'):
    """
    Configure virtualenvwrapper for the given user account.
    """
    home = c.run('getent passwd {} | cut -d: -f6'.format(user)).stdout.strip()
    home = home.rstrip('/')

    def update(script):
        script = '{}/{}'.format(home, script)
        if not exists(c, script):
            c.sudo('touch {}'.format(script))
            c.sudo('chown {}: {}'.format(user, script))

        if c.sudo("grep '^export WORKON_HOME.*' {}".format(script), warn=True).failed:
            c.sudo("""bash -c 'echo "export WORKON_HOME={}" >> {}'""".format(workon_home, script))
            c.sudo("""bash -c 'echo "source {}" >> {}'""".format(wrapper, script))
        else:
            c.sudo("sed -i.bak -e 's/^export WORKON_HOME=.*/export WORKON_HOME={}/' {}".format(
                workon_home.replace('/', '\\/'), script))

    update('.profile')
    update('.bashrc')
    c.sudo("bash -l -c 'whoami'", user=user)


def mkvirtualenv(c, name, workon_home='/srv/envs', python=None,
                 use_sudo=True, user=None, runas_user=None):
    """
    Make a new Python virtual environment.
    """
    cmd = 'mkvirtualenv {} {}'.format('--python={}'.format(python) if python else '', name)
    if use_sudo:
        kw = {}
        if runas_user:
            kw = {'user': runas_user}
        c.sudo("bash -l -c '{}'".format(cmd), **kw)
    else:
        # TODO: need to use `bash -l` for this too?
        c.run(cmd)


@contextmanager
def workon(c, name):
    """
    Context manager to prefix your command(s) with the ``workon`` command.
    """
    with c.prefix('workon {}'.format(name)):
        yield


@contextmanager
def cdvirtualenv(c, name, subdirs=[], workon_home='/srv/envs'):
    """
    Context manager to prefix your command(s) with the ``cdvirtualenv`` command.
    """
    if isinstance(subdirs, six.string_types):
        subdirs = [subdirs]
    path = '{}/{}'.format(workon_home, name)
    if subdirs:
        path = '{}/{}'.format(path, '/'.join(subdirs))
    with workon(c, name):
        with c.cd(path):
            yield
