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
Fabric Library for SSH
"""

from __future__ import unicode_literals, absolute_import


def cache_host_key(c, host, for_user='root'):
    """
    Cache the SSH host key for the given host, for the given user.
    """
    cmd = 'ssh -o StrictHostKeyChecking=no {} echo'.format(host)
    user = None if for_user == 'root' else for_user
    c.sudo(cmd, user=user, warn=True)


def restart(c):
    """
    Restart the OpenSSH service
    """
    c.sudo('systemctl restart ssh.service')


def configure(c, allow_root=False):
    """
    Configure the OpenSSH service
    """
    path = '/etc/ssh/sshd_config'

    # PermitRootLogin no (or without-password)
    if c.run("grep '^PermitRootLogin ' {}".format(path), warn=True).failed:
        c.sudo('sed -i.bak -e "s/^#PermitRootLogin .*/PermitRootLogin {}/" {}'.format(
            'without-password' if allow_root else 'no', path))
    else:
        c.sudo('sed -i.bak -e "s/^PermitRootLogin .*/PermitRootLogin {}/" {}'.format(
            'without-password' if allow_root else 'no', path))

    # PasswordAuthentication no
    if c.run("grep '^PasswordAuthentication ' {}".format(path), warn=True).failed:
        c.sudo('sed -i.bak -e "s/^#?PasswordAuthentication .*/PasswordAuthentication no/" {}'.format(path))
    else:
        c.sudo('sed -i.bak -e "s/^PasswordAuthentication .*/PasswordAuthentication no/" {}'.format(path))

    restart(c)
