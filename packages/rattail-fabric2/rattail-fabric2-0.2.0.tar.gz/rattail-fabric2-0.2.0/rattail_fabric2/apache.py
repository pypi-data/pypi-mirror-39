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
Fabric library for Apache web server
"""

from __future__ import unicode_literals, absolute_import

import re

from rattail_fabric2 import apt


def install(c):
    """
    Install the Apache web service
    """
    apt.install(c, 'apache2')


def get_version(c):
    """
    Fetch the version of Apache running on the target system
    """
    result = c.sudo('apache2 -v')
    if not result.failed:
        match = re.match(r'^Server version: Apache/(\d+\.\d+)\.\d+ \(.*\)', result.stdout)
        if match:
            return float(match.group(1))


def enable_mod(c, *names):
    """
    Enable the given Apache modules
    """
    for name in names:
        c.sudo('a2enmod {}'.format(name))


def enable_site(c, *names):
    """
    Enable the given Apache site(s)
    """
    for name in names:
        c.sudo('a2ensite {}'.format(name))


def deploy_site(c, deployer, local_path, name, enable=False, **kwargs):
    """
    Deploy a file to Apache sites-available
    """
    apache_version = get_version(c)
    if apache_version == 2.2:
        path = '/etc/apache2/sites-available/{}'.format(name)
    else:
        path = '/etc/apache2/sites-available/{}.conf'.format(
            '000-default' if name == 'default' else name)
    context = kwargs.pop('context', {})
    context['apache_version'] = apache_version
    deployer(c, local_path, path, context=context, **kwargs)
    if enable and name != 'default':
        enable_site(c, name)


def restart(c):
    """
    Restart the Apache web service
    """
    c.sudo('systemctl restart apache2.service')
