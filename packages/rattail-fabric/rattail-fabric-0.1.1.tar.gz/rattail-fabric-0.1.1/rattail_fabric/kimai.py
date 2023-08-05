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
Fabric library for Kimai
"""

from __future__ import unicode_literals, absolute_import

from fabric.api import cd, sudo
from fabric.contrib.files import exists

from rattail_fabric import mkdir


def install_kimai(rootdir, version='1.3.1', user='www-data'):
    """
    Deploy the given version of Kimai to the given location.
    """
    mkdir(rootdir)
    with cd(rootdir):
        if not exists('kimai-{}'.format(version)):
            if not exists('kimai_{}.zip'.format(version)):
                sudo('wget https://github.com/kimai/kimai/releases/download/{0}/kimai_{0}.zip'.format(version))
            sudo('unzip kimai_{0}.zip -d kimai-{0}'.format(version))
            sudo('chown -R www-data: kimai-{}'.format(version))
            sudo('ln -sf kimai-{} kimai'.format(version))
            sudo('rm -rf kimai/installer kimai/updater')
