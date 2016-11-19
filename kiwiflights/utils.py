#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ####################################################################
# Copyright (C) 2016  Fridolin Pokorny, fridex.devel@gmail.com
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# ####################################################################
"""Utils and helpers for kiwiflights"""

# We could use ujson
import json


def datetime_format(datetime_instance):
    """A helper to unify output datetime representation

    :param datetime_instance: datetime instance
    :type datetime_instance: datetime.datetime
    :return: a string representation of datetime
    """
    return datetime_instance.strftime('%Y-%m-%dT%H:%M:%S')


def dict2json(dict_, pretty=True):
    """"Convert dict to a human readable JSON

    :param dict_: dict that should be converted
    :type dict_: dict
    :param pretty: use pretty formatting
    :type pretty: bool
    :return: serialized dict into JSON in a human readable form
    :rtype: bool
    """
    if pretty is True:
        return json.dumps(dict_, sort_keys=True, separators=(',', ': '), indent=2)
    else:
        return json.dumps(dict_)
