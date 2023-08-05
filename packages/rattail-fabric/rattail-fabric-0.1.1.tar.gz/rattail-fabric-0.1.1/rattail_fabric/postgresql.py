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

import os
import re

from fabric.api import sudo, run, get, hide, abort, put, local

from rattail_fabric import apt


def install():
    """
    Install the PostgreSQL database service
    """
    apt.install('postgresql')


def get_version():
    """
    Fetch the version of PostgreSQL running on the target system
    """
    result = sudo('psql --version')
    if result.succeeded:
        match = re.match(r'^psql \(PostgreSQL\) (\d+\.\d+)(?:\.\d+)?', result)
        if match:
            return float(match.group(1))


def sql(sql, database='', port=None):
    """
    Execute some SQL as the 'postgres' user.
    """
    cmd = 'sudo -u postgres psql {port} --tuples-only --no-align --command="{sql}" {database}'.format(
        port='--port={}'.format(port) if port else '',
        sql=sql, database=database)
    return sudo(cmd, shell=False)


def script(path, database='', port=None, user=None, password=None):
    """
    Execute a SQL script.  By default this will run as 'postgres' user, but can
    use PGPASSWORD authentication if necessary.
    """
    port = '--port={}'.format(port) if port else ''
    if user and password:
        with hide('running'):
            kw = dict(pw=password, user=user, port=port, path=path, db=database)
            return sudo(" PGPASSWORD='{pw}' psql --host=localhost {port} --username='{user}' --file='{path}' {db}".format(**kw))

    else: # run as postgres
        kw = dict(port=port, path=path, db=database)
        return sudo("sudo -u postgres psql {port} --file='{path}' {db}".format(**kw), shell=False)


def user_exists(name, port=None):
    """
    Determine if a given PostgreSQL user exists.
    """
    user = sql("SELECT rolname FROM pg_roles WHERE rolname = '{0}'".format(name), port=port)
    return bool(user)


def create_user(name, password=None, port=None, checkfirst=True, createdb=False):
    """
    Create a PostgreSQL user account.
    """
    if not checkfirst or not user_exists(name, port=port):
        sudo('sudo -u postgres createuser {port} {createdb} --no-createrole --no-superuser {name}'.format(
            port='--port={}'.format(port) if port else '',
            createdb='--{}createdb'.format('' if createdb else 'no-'),
            name=name))
        if password:
            set_user_password(name, password, port=port)


def set_user_password(name, password, port=None):
    """
    Set the password for a PostgreSQL user account
    """
    with hide('running'):
        sql("ALTER USER \\\"{}\\\" PASSWORD '{}';".format(name, password), port=port)


def db_exists(name, port=None):
    """
    Determine if a given PostgreSQL database exists.
    """
    db = sql("SELECT datname FROM pg_database WHERE datname = '{0}'".format(name), port=port)
    return db == name


def create_db(name, owner=None, port=None, checkfirst=True):
    """
    Create a PostgreSQL database.
    """
    if not checkfirst or not db_exists(name, port=port):
        cmd = 'sudo -u postgres createdb {port} {owner} {name}'.format(
            port='--port={}'.format(port) if port else '',
            owner='--owner={}'.format(owner) if owner else '',
            name=name)
        sudo(cmd, shell=False)


def create_schema(name, dbname, owner='rattail', port=None):
    """
    Create a schema within a PostgreSQL database.
    """
    sql_ = "create schema if not exists {} authorization {}".format(name, owner)
    sql(sql_, database=dbname, port=port)


def drop_db(name, checkfirst=True):
    """
    Drop a PostgreSQL database.
    """
    if not checkfirst or db_exists(name):
        sudo('sudo -u postgres dropdb {0}'.format(name), shell=False)


def download_db(name, destination=None, port=None, exclude_tables=None):
    """
    Download a database from the "current" server.
    """
    if destination is None:
        destination = './{0}.sql.gz'.format(name)
    run('touch {0}.sql'.format(name))
    run('chmod 0666 {0}.sql'.format(name))
    sudo('sudo -u postgres pg_dump {port} {exclude_tables} --file={name}.sql {name}'.format(
        name=name,
        port='--port={}'.format(port) if port else '',
        exclude_tables='--exclude-table-data={}'.format(exclude_tables) if exclude_tables else '',
    ), shell=False)
    run('gzip --force {0}.sql'.format(name))
    get('{0}.sql.gz'.format(name), destination)
    run('rm {0}.sql.gz'.format(name))


def clone_db(name, owner, download, user='rattail', force=False, workdir=None):
    """
    Clone a database from a (presumably live) server

    :param name: Name of the database.

    :param owner: Username of the user who is to own the database.

    :param force: Whether the target database should be forcibly dropped, if it
       exists already.
    """
    if db_exists(name):
       if force:
           drop_db(name, checkfirst=False)
       else:
           abort("Database '{}' already exists!".format(name))

    create_db(name, owner=owner, checkfirst=False)

    # upload database dump to target server
    if workdir:
        curdir = os.getcwd()
        os.chdir(workdir)
    download('{}.sql.gz'.format(name), user=user)
    put('{}.sql.gz'.format(name))
    local('rm {}.sql.gz'.format(name))
    if workdir:
        os.chdir(curdir)

    # restore database on target server
    run('gunzip --force {}.sql.gz'.format(name))
    sudo('sudo -u postgres psql --echo-errors --file={0}.sql {0}'.format(name), shell=False)
    run('rm {}.sql'.format(name))
