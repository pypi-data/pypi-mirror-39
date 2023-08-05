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
Fabric Library for PostgreSQL
"""

from __future__ import unicode_literals, absolute_import

from rattail_fabric2 import apt


def install(c):
    """
    Install the PostgreSQL database service
    """
    apt.install(c, 'postgresql')


def sql(c, sql, database='', port=None):
    """
    Execute some SQL as the 'postgres' user.
    """
    cmd = 'sudo -u postgres psql {port} --tuples-only --no-align --command="{sql}" {database}'.format(
        port='--port={}'.format(port) if port else '',
        sql=sql, database=database)
    return c.sudo(cmd, shell=False)


def user_exists(c, name, port=None):
    """
    Determine if a given PostgreSQL user exists.
    """
    user = sql(c, "SELECT rolname FROM pg_roles WHERE rolname = '{0}'".format(name), port=port).stdout.strip()
    return bool(user)


def create_user(c, name, password=None, port=None, checkfirst=True, createdb=False):
    """
    Create a PostgreSQL user account.
    """
    if not checkfirst or not user_exists(c, name, port=port):
        c.sudo('sudo -u postgres createuser {port} {createdb} --no-createrole --no-superuser {name}'.format(
            port='--port={}'.format(port) if port else '',
            createdb='--{}createdb'.format('' if createdb else 'no-'),
            name=name))
        if password:
            set_user_password(c, name, password, port=port)


def set_user_password(c, name, password, port=None):
    """
    Set the password for a PostgreSQL user account
    """
    # TODO: probably should figure out how to suppress echo for this command
    # with hide('running'):
    sql(c, "ALTER USER \\\"{}\\\" PASSWORD '{}';".format(name, password), port=port)


def db_exists(c, name, port=None):
    """
    Determine if a given PostgreSQL database exists.
    """
    db = sql(c, "SELECT datname FROM pg_database WHERE datname = '{0}'".format(name), port=port).stdout.strip()
    return db == name


def create_db(c, name, owner=None, port=None, checkfirst=True):
    """
    Create a PostgreSQL database.
    """
    if not checkfirst or not db_exists(c, name, port=port):
        cmd = 'sudo -u postgres createdb {port} {owner} {name}'.format(
            port='--port={}'.format(port) if port else '',
            owner='--owner={}'.format(owner) if owner else '',
            name=name)
        c.sudo(cmd)
