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
Fabric Library for FreeTDS
"""

from __future__ import unicode_literals, absolute_import

from fabric.api import cd, sudo
from fabric.contrib.files import exists

from rattail_fabric import apt, mkdir


def install_from_source(user='rattail'):
    """
    Install the FreeTDS library from source.

    Per instructions found here:
    https://github.com/FreeTDS/freetds/blob/master/INSTALL.GIT
    """
    apt.install(
        'automake',
        'autoconf',
        'gettext',
        'pkg-config',
    )

    with cd('/usr/local/src'):
        if not exists('freetds'):
            mkdir('freetds', owner=user)
            sudo('git clone https://github.com/FreeTDS/freetds.git', user=user)

    if not exists('/usr/local/lib/libtdsodbc.so'):
        with cd('/usr/local/src/freetds'):
            sudo('./autogen.sh', user=user)
            sudo('make', user=user)
            sudo('make install')
