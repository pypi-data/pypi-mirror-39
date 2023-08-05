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
Misc. Utilities
"""

from __future__ import unicode_literals, absolute_import


def is_win(c):
    """
    Return True if remote SSH server is running Windows, False otherwise.

    The idea is based on echoing quoted text: \*NIX systems will echo quoted
    text only, while Windows echoes quotation marks as well.

    .. note::

       This function is derived from one copied from fabric v1.
    """
    result = c.run('echo "Will you echo quotation marks"', warn=True)
    return '"' in result.stdout


def _expand_path(c, path):
    """
    Return a path expansion

    E.g.    ~/some/path     ->  /home/myuser/some/path
            /user/\*/share   ->  /user/local/share
    More examples can be found here: http://linuxcommand.org/lc3_lts0080.php

    .. versionchanged:: 1.0
        Avoid breaking remote Windows commands which does not support expansion.

    .. note::

       This function is derived from one copied from fabric v1.
    """
    return path if is_win(c) else '"$(echo %s)"' % path


def exists(c, path, use_sudo=False):
    """
    Return True if given path exists on the current remote host.

    If ``use_sudo`` is True, will use `sudo` instead of `run`.

    .. note::

       This function is derived from one copied from fabric v1.
    """
    func = c.sudo if use_sudo else c.run
    cmd = 'stat %s' % _expand_path(c, path)
    return not func(cmd, warn=True).failed
