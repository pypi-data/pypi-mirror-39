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
Fabric library for Luigi
"""

from __future__ import unicode_literals, absolute_import

import os

from rattail_fabric import make_deploy


deploy = make_deploy(__file__)


def deploy_logging_config(envroot):
    """
    Deploy common logging file for Luigi.
    """
    envroot = envroot.rstrip('/')
    deploy('luigi/luigi-logging.conf.mako', os.path.join(envroot, 'app', 'luigi', 'luigi-logging.conf'),
           context={'envroot': envroot})
