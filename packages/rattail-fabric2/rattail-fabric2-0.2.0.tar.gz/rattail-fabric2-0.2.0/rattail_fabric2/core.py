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
Core Utilities
"""

from __future__ import unicode_literals, absolute_import

import os
import re
import tempfile

import six

from mako.template import Template


def is_link(c, path, use_sudo=False):
    """
    Return True if the given path is a symlink on the current remote host.

    If ``use_sudo`` is True, will use `.sudo` instead of `.run`.

    .. note::

       This function is derived from one copied from fabric v1.
    """
    func = c.sudo if use_sudo else c.run
    cmd = 'test -L "$(echo %s)"' % path
    result = func(cmd)
    return False if result.failed else True


def get_debian_version(c):
    """
    Fetch the version of Debian running on the target system.
    """
    version = c.run('cat /etc/debian_version').stdout.strip()
    match = re.match(r'^(\d+\.\d+)$', version)
    if match:
        return float(match.group(1))


def get_ubuntu_version(c):
    """
    Fetch the version of Ubuntu running on the target system
    """
    info = c.run('cat /etc/lsb-release').stdout.strip()
    match = re.search(r'DISTRIB_RELEASE=(\d+\.\d+)', info)
    if match:
        return float(match.group(1))


def mkdir(c, paths, owner=None, mode=None,
          use_sudo=False, runas_user=None):
    """
    Recursively make one or more directories.
    """
    if isinstance(paths, six.string_types):
        paths = [paths]
    cmd = 'mkdir --parents {}'.format(' '.join(paths))
    if use_sudo:
        c.sudo(cmd, user=runas_user)
    else:
        c.run(cmd)
    if owner:
        if ':' not in owner:
            owner = '{0}:{0}'.format(owner)
        func = c.sudo if use_sudo else c.run
        func('chown {} {}'.format(owner, ' '.join(paths)))
    if mode is not None:
        func = c.sudo if use_sudo else c.run
        func('chmod {} {}'.format(mode, ' '.join(paths)))


def make_system_user(c, name, home=None, uid=None, shell=None):
    """
    Make a new system user account, with the given home folder and shell path.
    """
    if not c.run('getent passwd {}'.format(name), warn=True).failed:
        return

    home = '--home {}'.format(home) if home else ''
    uid = '--uid {}'.format(uid) if uid else ''
    shell = '--shell {}'.format(shell) if shell else ''
    c.sudo('adduser --system --group {} {} {} {}'.format(name, home, uid, shell))


def set_timezone(c, timezone):
    """
    Set the system timezone to the given value, e.g. 'America/Chicago'.
    """
    c.sudo("bash -c 'echo {} > /etc/timezone'".format(timezone))
    if is_link(c, '/etc/localtime'):
        c.sudo('ln --symbolic --force /usr/share/zoneinfo/{} /etc/localtime'.format(timezone))
    else:
        c.sudo('cp /usr/share/zoneinfo/{} /etc/localtime'.format(timezone))


def put(c, local_path, remote_path, owner=None, mode=None,
        use_sudo=False, **kwargs):
    """
    Put a file on the server, and set its ownership.
    """
    # TODO: are we mirroring now?
    # if 'mode' not in kwargs:
    #     kwargs.setdefault('mirror_local_mode', True)

    # upload file
    if use_sudo:
        tempdir = c.run('mktemp -d').stdout.strip()
        basename = os.path.basename(remote_path)
        temp_path = os.path.join(tempdir, basename)
        c.put(local_path, temp_path, **kwargs)
        # TODO: need to address single quotes within filename
        if not owner:
            c.sudo("chown root: '{}'".format(temp_path))
        c.sudo("mv '{}' '{}'".format(temp_path, remote_path))
        c.run('rmdir {}'.format(tempdir))
    else:
        c.put(local_path, remote_path, **kwargs)

    # set owner / mode if needed
    func = c.sudo if use_sudo else c.run
    if owner:
        if ':' not in owner:
            owner = '{}:'.format(owner)
        func("chown {} '{}'".format(owner, remote_path))
    if mode:
        func("chmod {} '{}'".format(mode, remote_path))


def upload_mako_template(c, local_path, remote_path, context={},
                         encoding='utf_8', **kwargs):
    """
    Render a local file as a Mako template, and upload the result to the server.
    """
    template = Template(filename=local_path)

    temp_dir = tempfile.mkdtemp(prefix='rattail-fabric.')
    temp_path = os.path.join(temp_dir, os.path.basename(local_path))
    text = template.render(**context)
    if six.PY3:
        with open(temp_path, 'wt', encoding=encoding) as f:
            f.write(text)
    else:
        with open(temp_path, 'wb') as f:
            f.write(text.encode(encoding))
    os.chmod(temp_path, os.stat(local_path).st_mode)

    put(c, temp_path, remote_path, **kwargs)
    os.remove(temp_path)
    os.rmdir(temp_dir)


class Deployer(object):

    def __init__(self, deploy_path, last_segment='deploy'):
        if not os.path.isdir(deploy_path):
            deploy_path = os.path.abspath(os.path.join(os.path.dirname(deploy_path), last_segment))
        self.deploy_path = deploy_path

    def __call__(self, c, local_path, remote_path, **kwargs):
        self.deploy(c, local_path, remote_path, **kwargs)

    def full_path(self, local_path):
        return '{}/{}'.format(self.deploy_path, local_path)

    def deploy(self, c, local_path, remote_path, context={}, **kwargs):
        local_path = self.full_path(local_path)
        if local_path.endswith('.template'):
            raise NotImplementedError
        elif local_path.endswith('.mako'):
            upload_mako_template(c, local_path, remote_path, context=context, **kwargs)
        else:
            put(c, local_path, remote_path, **kwargs)

    def sudoers(self, c, local_path, remote_path, owner='root:', mode='0440', **kwargs):
        self.deploy(c, local_path, '/tmp/sudoers', owner=owner, mode=mode, use_sudo=True)
        c.sudo('mv /tmp/sudoers {}'.format(remote_path))

    def apache_site(self, c, local_path, name, **kwargs):
        from rattail_fabric2.apache import deploy_site
        kwargs['use_sudo'] = True
        deploy_site(c, self, local_path, name, **kwargs)


def make_deploy(deploy_path, last_segment='deploy'):
    """
    Make a ``deploy()`` function, for uploading files to the server.

    During a deployment, one usually needs to upload certain additional files
    to the server.  It's also often necessary to dynamically define certain
    settings etc. within these files.  The :func:`upload_template()` and
    :func:`put()` functions, respectively, handle uploading files which do and
    do not require dynamic variable substitution.

    The return value from ``make_deploy()`` is a function which will call
    ``put()`` or ``upload_template()`` based on whether or not the file path
    ends with ``'.template'``.

    To make the ``deploy()`` function even simpler for the caller, it will
    assume a certain context for local file paths.  This means one only need
    provide a base file name when calling ``deploy()``, and it will be
    interpreted as relative to the function's context path.

    The ``deploy_path`` argument is used to establish the context path for the
    function.  If it is a folder path, it will be used as-is; otherwise it will
    be constructed by joining the parent folder of ``deploy_path`` with the
    value of ``last_segment``.

    Typical usage then is something like::

       from rattail_fabric import make_deploy

       deploy = make_deploy(__file__)

       deploy('rattail/init-filemon', '/etc/init.d/rattail-filemon',
              mode='0755')

       deploy('rattail/rattail.conf.template', '/etc/rattail.conf')

    This shows what is intended to be typical, i.e. where ``__file__`` is the
    only argument required for ``make_deploy()``.  For the above to work will
    require you to have something like this file structure, where
    ``fabfile.py`` is the script which contains the above code::

       myproject/
       |-- fabfile.py
       |-- deploy/
           `-- rattail/
               |-- init-filemon
               |-- rattail.conf.template
    """
    return Deployer(deploy_path, last_segment)
