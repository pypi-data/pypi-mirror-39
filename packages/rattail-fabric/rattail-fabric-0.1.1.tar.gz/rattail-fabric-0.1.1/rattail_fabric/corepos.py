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
Fabric library for CORE-POS (IS4C)
"""

from __future__ import unicode_literals, absolute_import

import webbrowser

from fabric.api import sudo, cd, env, run
from fabric.contrib.files import exists

from rattail_fabric import apt, mysql, mkdir
from rattail_fabric import make_deploy


deploy = make_deploy(__file__)


def install_fannie(rootdir, user='www-data', branch='version-2.3', first_time=None, url=None):
    """
    Install the Fannie app to the given location.

    Please note, this assumes composer is already installed and available.
    """
    if first_time is None:
        first_time = not exists(rootdir)
    mkdir(rootdir, owner=user)
    with cd(rootdir):

        # fannie source
        if not exists('IS4C'):
            sudo('git clone https://github.com/CORE-POS/IS4C.git', user=user)
            with cd('IS4C'):
                sudo('git checkout {}'.format(branch), user=user)
        with cd('IS4C'):
            sudo('git pull', user=user)

        if user == 'www-data':
            # TODO: why is this necessary? (but it is, nonetheless)
            mkdir('/var/www/.composer', owner=user)

        # fannie dependencies
        with cd('IS4C'):
            mkdir(['vendor', 'fannie/src/javascript/composer-components'], owner=user)
            sudo('composer.phar install', user=user)

        # shadowread
        with cd('IS4C/fannie/auth/shadowread'):
            sudo('make')
            sudo('make install')

        # fannie config
        with cd('IS4C/fannie'):
            if not exists('config.php'):
                deploy('corepos/fannie/config.php.mako', 'config.php', owner=user, mode='0600')

        # fannie logging
        with cd('IS4C/fannie/logs'):
            for name in ['fannie', 'debug_fannie', 'queries', 'php-errors', 'dayend']:
                sudo('touch {}.log'.format(name), user=user)

    # fannie databases
    mysql.create_user('is4c', host='%', password='is4c')
    mysql.create_db('core_op', user="is4c@'%'")
    mysql.create_db('core_trans', user="is4c@'%'")
    mysql.create_db('trans_archive', user="is4c@'%'")

    # fannie web installer
    if first_time:
        url = url or getattr(env, 'fannie_rooturl', 'http://localhost/fannie/')
        webbrowser.open_new_tab('{}/install/'.format(url.rstrip('/')))
