# -*- coding: utf-8 -*-
# Description:
# Setup for the OSP nmap Server
#
# Authors:
# Juan José Nicola <juan.nicola@greenbone.net>
#
# Copyright:
# Copyright (C) 2018 Greenbone Networks GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

""" Function related to the NVT information. """

# Needed to say that when we import ospd, we mean the package and not the
# module in that directory.
from __future__ import absolute_import
from __future__ import print_function

import ospd.kb as kb

NVTICACHE_STR = 'nvticache10'

def get_feed_version():
    """ Get feed version.
    """
    return kb.item_get_single(NVTICACHE_STR)

def get_oids():
    """ Get the list of NVT OIDs.
    """
    ctx = kb.db_find("nvticache10")
    kb.set_global_redisctx(ctx)
    return kb.get_pattern('filename:*:oid')
