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

import os
from contextlib import contextmanager

import six

from fabric.api import abort, sudo, run, prefix, cd, settings, env
from fabric.contrib.files import exists, append

from rattail_fabric import apt, mkdir


def install_pip(use_apt=False, eager=True):
    """
    Install/upgrade the Pip installer for Python.
    """
    if use_apt:
        apt.install('python-pip')
    else:
        apt.install('build-essential', 'python-dev', 'libssl-dev', 'libffi-dev')
        with settings(warn_only=True):
            result = sudo('which pip')
        if result.failed:
            apt.install('python-pkg-resources', 'python-setuptools')
            sudo('easy_install pip')
            sudo('apt-get --assume-yes purge python-setuptools')
            pip('setuptools')
        pip('pip', upgrade=True)
        kwargs = {}
        if eager:
            kwargs['upgrade_strategy'] = 'eager'
        pip('setuptools', 'wheel', 'ndg-httpsclient', upgrade=True, **kwargs)


def pip(*packages, **kwargs):
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
        abort("Unknown kwargs for pip(): {}".format(kwargs))
    packages = ["'{}'".format(p) for p in packages]
    cmd = 'pip install {} {} {}'.format(upgrade, upgrade_strategy, ' '.join(packages))
    if use_sudo:
        kw = {}
        if runas_user:
            kw['user'] = runas_user
        sudo(cmd, **kw)
    else:
        run(cmd)


def install_virtualenvwrapper(workon_home=None, user='root', use_apt=False, configure_me=True):
    """
    Install the `virtualenvwrapper`_ system, with the given ``workon`` home,
    owned by the given user.
    """
    workon_home = workon_home or getattr(env, 'python_workon_home', '/srv/envs')
    mkdir(workon_home, owner=user)
    if use_apt:
        apt.install('virtualenvwrapper')
    else:
        pip('virtualenvwrapper', upgrade=True)
        configure_virtualenvwrapper(user, workon_home)
        if configure_me:
            configure_virtualenvwrapper(env.user, workon_home)


def configure_virtualenvwrapper(user, workon_home=None, wrapper='/usr/local/bin/virtualenvwrapper.sh'):
    """
    Configure virtualenvwrapper for the given user account.
    """
    workon_home = workon_home or getattr(env, 'python_workon_home', '/srv/envs')
    home = sudo('getent passwd {} | cut -d: -f6'.format(user))
    home = home.rstrip('/')

    def update(script):
        script = '{}/{}'.format(home, script)
        if not exists(script):
            sudo('touch {}'.format(script))
            sudo('chown {}: {}'.format(user, script))
        append(script, 'export WORKON_HOME={}'.format(workon_home), use_sudo=True)
        append(script, 'source {}'.format(wrapper), use_sudo=True)

    update('.profile')
    update('.bashrc')
    sudo('whoami', user=user) # no-op to trigger first hooks


def mkvirtualenv(name, python=None, use_sudo=True, user=None, runas_user=None, workon_home=None,
                 upgrade_pip=True, upgrade_six=True, upgrade_setuptools=True, upgrade_strategy=None):
    """
    Make a new Python virtual environment.
    """
    workon_home = workon_home or getattr(env, 'python_workon_home', '/srv/envs')
    cmd = 'mkvirtualenv {} {}'.format('--python={}'.format(python) if python else '', name)
    if use_sudo:
        kw = {}
        if runas_user:
            kw = {'user': runas_user}
        sudo(cmd, **kw)
    else:
        run(cmd)
    if upgrade_pip:
        if isinstance(upgrade_pip, six.string_types):
            pip_req = upgrade_pip
        else:
            pip_req = 'pip'
        with workon(name):
            if upgrade_six:
                pip('six', upgrade=True, use_sudo=use_sudo, runas_user=runas_user)
            pip(pip_req, upgrade=True, use_sudo=use_sudo, runas_user=runas_user)
            if upgrade_setuptools:
                pip('setuptools', 'wheel', 'ndg-httpsclient',
                    upgrade=True, upgrade_strategy=upgrade_strategy,
                    use_sudo=use_sudo, runas_user=runas_user)
    if user:
        with cd(os.path.join(workon_home, name)):
            mkdir('app/log', owner='{0}:{0}'.format(user))
        if use_sudo and runas_user:
            sudo('chown {}: /srv/envs/{}/app'.format(runas_user, name))


@contextmanager
def workon(name):
    """
    Context manager to prefix your command(s) with the ``workon`` command.
    """
    with prefix('workon {0}'.format(name)):
        yield


@contextmanager
def cdvirtualenv(name, subdirs=[], workon_home=None):
    """
    Context manager to prefix your command(s) with the ``cdvirtualenv`` command.
    """
    workon_home = workon_home or getattr(env, 'python_workon_home', '/srv/envs')
    if isinstance(subdirs, six.string_types):
        subdirs = [subdirs]
    path = '{0}/{1}'.format(workon_home, name)
    if subdirs:
        path = '{0}/{1}'.format(path, '/'.join(subdirs))
    with workon(name):
        with cd(path):
            yield
