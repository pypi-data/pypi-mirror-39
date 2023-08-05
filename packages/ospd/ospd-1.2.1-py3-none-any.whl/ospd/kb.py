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

""" Functios to retrieve and store in Redis kb. """

# Needed to say that when we import ospd, we mean the package and not the
# module in that directory.
from __future__ import absolute_import
from __future__ import print_function

import redis
import subprocess
import string
import xml.etree.ElementTree as ET


""" Path to the Redis socket. """
KB_LOCATION = ""

""" Name of the namespace usage bitmap in redis. """
DBINDEX_NAME = "GVM.__GlobalDBIndex"
MAX_DBINDEX = 0
DB_INDEX = 0
REDISCONTEXT = None
SOCKET_TIMEOUT = 60

# Possible positions of nvt values in cache list.
nvt_meta_fields = [
    "NVT_FILENAME_POS",
    "NVT_REQUIRED_KEYS_POS",
    "NVT_MANDATORY_KEYS_POS",
    "NVT_EXCLUDED_KEYS_POS",
    "NVT_REQUIRED_UDP_PORTS_POS",
    "NVT_REQUIRED_PORTS_POS",
    "NVT_DEPENDENCIES_POS",
    "NVT_TAGS_POS",
    "NVT_CVES_POS",
    "NVT_BIDS_POS",
    "NVT_XREFS_POS",
    "NVT_CATEGORY_POS",
    "NVT_TIMEOUT_POS",
    "NVT_FAMILY_POS",
    "NVT_COPYRIGHT_POS",
    "NVT_NAME_POS",
    "NVT_VERSION_POS",]

def get_kb_location():
    """ Retrive the kb location from openvassd config.
    """
    global KB_LOCATION
    try:
        result = subprocess.check_output(['openvassd', '-s'],
                                         stderr=subprocess.STDOUT)
        result = result.decode('ascii')
    except OSError:
        # the command is not available
        return 2

    if result is None:
        return 2

    kbpath = None
    for conf in result.split('\n'):
        if conf.find("kb_location") == 0:
            kbpath = conf.split('=')
            break

    if kbpath is None:
        return 2

    KB_LOCATION = str.strip(kbpath[1])


def max_db_index():
    """Set the number of databases have been configured
        into kbr struct.
    """
    global MAX_DBINDEX
    try:
        ctx = kb_connect()
        resp = ctx.config_get("databases")
    except RedisError:
        return 2

    if isinstance(resp, dict) is False:
        return 2
    if len(resp) == 1:
        MAX_DBINDEX = int(resp["databases"])
    else:
        print("KB Redis: unexpected reply length %d" % len(resp))
        return 2

def set_global_redisctx(ctx):
    """ Set the global set the global REDISCONTEXT.
    """
    global REDISCONTEXT
    REDISCONTEXT = ctx

def kb_init():
    """ Set kb_location and max_db_index. """
    if get_kb_location() or max_db_index():
        return False
    return True

def try_database_index(ctx, i):
    """ Check if it is already in use. If not set it as in use and return.
    """
    try:
        resp = ctx.hsetnx(DBINDEX_NAME, i, 1)
    except:
        return 2

    if isinstance(resp, int) is False:
        return 2

    if resp == 1:
        return 1

def kb_connect(dbnum=0):
    """ Connect to redis to the given database or to the default db 0 .
    """
    global DB_INDEX
    if get_kb_location() is 2:
        return 2
    try:
        ctx = redis.Redis(unix_socket_path=KB_LOCATION,
                          db=dbnum,
                          socket_timeout=SOCKET_TIMEOUT, charset="latin-1", decode_responses=True)
    except ConnectionError as e:
        return {"error": str(e)}
    DB_INDEX = dbnum
    return ctx

def db_find(patt):
    """ Search a pattern inside all kbs. When find it
        return it.
    """
    for i in range(0, MAX_DBINDEX):
        ctx = kb_connect (i)
        if ctx.keys(patt):
            return ctx

def kb_new():
    """ Return a new kb context to an empty kb.
    """
    ctx = db_find(DBINDEX_NAME)
    for index in range(1, MAX_DBINDEX):
            if try_database_index(ctx, index) == 1:
                ctx = kb_connect(index)
                return ctx

def select_database(ctx):
    """ Given a Redis context, it will select the DB.
    """
    global MAX_DBINDEX
    if DB_INDEX == 0:
        if MAX_DBINDEX == 0:
            if max_db_index() == 2:
               return 2

        for i in range(1, MAX_DBINDEX):
            if try_database_index(ctx, i) == 1:
                break

    if DB_INDEX == 0:
        print("Not possible to select a free DB")
        return 2

def get_kb_context():
    """ Get redis context if it is already connected or do a
        a connection.
    """
    global REDISCONTEXT
    if REDISCONTEXT is not None:
        return REDISCONTEXT

    REDISCONTEXT = db_find(DBINDEX_NAME)

    if REDISCONTEXT is None:
        print("Problem retrieving Redis Context")
        return 2

    return REDISCONTEXT

def item_get_set(name):
    """ Get all values under a KB elements.
    The right global REDISCONTEXT must be already set.
    """
    ctx = get_kb_context()
    return ctx.smembers(name)

def item_get_single(name):
    """ Get a single KB element. The right global REDISCONTEXT must be
    already set.
    """
    ctx = get_kb_context()
    return ctx.srandmember(name)

def item_add_single(name, values):
    """ Add a single KB element with one or more values.
    The right global REDISCONTEXT must be already set.
    """
    ctx = get_kb_context()
    ctx.sadd(name, *set(values))

def item_set_single(name, value):
    """ Set (replace) a new single KB element. The right global
    REDISCONTEXT must be already set.
    """
    ctx = get_kb_context()
    pipe = ctx.pipeline()
    pipe.delete(name)
    pipe.sadd(name, value)

def item_del_single(name):
    """ Delete a single KB element. The right global REDISCONTEXT must be
    already set.
    """
    ctx = get_kb_context()
    ctx.delete(name)

def get_nvt_pref(oid):
    """ Get NVT's preferences.
        @Return XML tree with preferences
    """
    ctx = get_kb_context()
    resp = ctx.smembers('oid:%s:prefs' % oid)
    timeout = ctx.lindex('nvt:%s' % oid,
                         nvt_meta_fields.index("NVT_TIMEOUT_POS"))
    preferences = ET.Element('preferences')
    if timeout > 0:
        xml_timeout = ET.Element('timeout')
        xml_timeout.text = timeout
        preferences.append(xml_timeout)

    if len(resp) > 0:
        for nvt_pref in resp:
            elem = nvt_pref.split('|||')
            preference = ET.Element('preference')
            xml_name = ET.SubElement(preference, 'name')
            xml_name.text = elem[0]
            xml_type = ET.SubElement(preference, 'type')
            xml_type.text = elem[1]
            if elem[2]:
                xml_def = ET.SubElement(preference, 'default')
                xml_def.text = elem[2]
            preferences.append(preference)

    return preferences

def get_nvt_all(oid):
    """ Get a full NVT. Returns an XML tree with the NVT metadata.
    """
    ctx = get_kb_context()
    resp = ctx.lrange("nvt:%s" % oid,
                      nvt_meta_fields.index("NVT_FILENAME_POS"),
                      nvt_meta_fields.index("NVT_VERSION_POS"))

    if (isinstance(resp, list) and len(resp) > 0) is False:
        return None

    nvt = ET.Element('nvt')
    nvt.set('oid', oid)

    subelem = ['file_name', 'required_keys', 'mandatory_keys',
               'excluded_keys', 'required_udp_ports', 'required_ports',
               'dependencies', 'tag', 'cve', 'bid', 'xref', 'category',
               'timeout', 'family', 'copyright', 'name', 'version']

    for elem in subelem:
        ET.SubElement(nvt, elem)
    for child, res in zip(nvt.getchildren(), resp):
        child.text = res.decode('latin-1')

    # Add preferences
    nvt.append(get_nvt_pref(oid))

    return nvt

def get_pattern(pattern):
    """ Get all items stored under a given pattern.
    """
    ctx = get_kb_context()
    items = ctx.keys(pattern)

    elem_list = []
    for item in items:
        elem_list.append(ctx.smembers(item))
    return elem_list

def release_db(kbindex=0):
    """ Connect to redis and select the db by index.
        Flush db and delete the index from DBINDEX_NAME list.
    """
    if kbindex:
        ctx = kb_connect(kbindex)
        ctx.flushdb()
        ctx = kb_connect()
        ctx.hdel(DBINDEX_NAME, kbindex)

def get_result():
    """ Get and remove the oldest result from the list. """
    ctx = get_kb_context()
    return ctx.rpop("internal/results")

def get_status():
    """ Get and remove the oldest host scan status from the list. """
    ctx = get_kb_context()
    return ctx.rpop("internal/status")

def get_host_scan_scan_start_time():
    """ Get the timestamp of the scan start from redis. """
    ctx = get_kb_context()
    return ctx.rpop("internal/start_time")

def get_host_scan_scan_end_time():
    """ Get the timestamp of the scan end from redis. """
    ctx = get_kb_context()
    return ctx.rpop("internal/end_time")
