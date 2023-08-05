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
Fabric library for Backup app
"""

from __future__ import unicode_literals, absolute_import

import datetime

from fabric.api import cd, sudo
from fabric.contrib.files import exists

from rattail_fabric import make_deploy, mkdir, python, UNSPECIFIED


deploy_generic = make_deploy(__file__)


def deploy_backup_everything(**context):
    """
    Deploy the generic `backup-everything` script
    """
    context.setdefault('envname', 'backup')
    context.setdefault('user', 'rattail')
    deploy_generic('backup/backup-everything.mako', '/usr/local/bin/backup-everything', mode='0700',
                   context=context)


def deploy_backup_app(deploy, envname, mkvirtualenv=True, user='rattail',
                      config=None, everything=None, crontab=None, runat=UNSPECIFIED):
    """
    Make an app which can run backups for the server.
    """
    if not config:
        path = '{}/rattail.conf'.format(envname)
        if deploy.local_exists(path):
            config = path
        else:
            raise ValueError("Must provide config path for backup app")

    if runat is UNSPECIFIED:
        runat = datetime.time(0) # defaults to midnight

    # virtualenv
    if mkvirtualenv:
        python.mkvirtualenv(envname, python='/usr/bin/python3', upgrade_setuptools=False)
    envpath = '/srv/envs/{}'.format(envname)
    sudo('chown -R {}: {}'.format(user, envpath))
    with cd(envpath):
        mkdir('src', owner=user)
        sudo('bin/pip install --upgrade pip', user=user)

        # rattail
        if not exists('src/rattail'):
            sudo('git clone https://rattailproject.org/git/rattail.git src/rattail', user=user)
        with cd('src/rattail'):
            sudo('git pull', user=user)
            deploy_generic('backup/git-exclude', '.git/info/exclude', owner=user)
        sudo('bin/pip install --upgrade --upgrade-strategy eager --editable src/rattail', user=user)

        # config
        sudo('bin/rattail make-appdir', user=user)
        deploy(config, 'app/rattail.conf', owner=user, mode='0600')
        sudo('bin/rattail -c app/rattail.conf make-config -T quiet -O app/', user=user)
        sudo('bin/rattail -c app/rattail.conf make-config -T silent -O app/', user=user)

    # backup-everything script
    everything_context = {
        'envname': envname,
        'user': user,
    }
    if everything:
        deploy(everything, '/usr/local/bin/backup-everything', mode='0700', context=everything_context)
    else:
        deploy_backup_everything(**everything_context)

    # crontab
    if runat:
        crontab_context = {
            'envname': envname,
            'pretty_time': runat.strftime('%I:%M %p'),
            'cron_time': runat.strftime('%M %H'),
        }
        if crontab:
            deploy(crontab, '/etc/cron.d/backup', context=crontab_context)
        else:
            deploy_generic('backup/crontab.mako', '/etc/cron.d/backup', context=crontab_context)
