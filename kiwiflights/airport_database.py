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
"""Airport database representation"""

import logging
from .airport import Airport

_logger = logging.getLogger(__name__)


class AirportDatabase(object):
    """Database for available airports"""
    def __init__(self, airports=None):
        """
        :param airports: a list of available airports
        :type airports: list(Airport)
        """
        self._airports = airports or []
        self._mapping = {}

        for airport in self._airports:
            if airport.code in self._mapping:
                raise ValueError("Multiple airports with same code provided, "
                                 "code %s" % airport.code)
            self._mapping[airport.code] = airport

    def __str__(self):
        return str(list(self._mapping.keys()))

    @property
    def airports(self):
        """
        :return: all airports available in the database
        :rtype: list(Airport)
        """
        return self._airports

    def to_csv(self):
        """
        :return: CSV representation of airport database
        """
        header = "airport\n"
        return header + "".join([a.code for a in self._airports])

    def to_dict(self):
        """
        :return: dict representation of available airports
        """
        return {'airports': [{'code': a.code for a in self._airports}]}

    def register(self, airport):
        """Register an airport to database

        :param airport: airport to be registered
        """
        _logger.debug("Registering airport '%s' to airport database", airport.code)

        if airport.code in self._mapping:
            raise ValueError("Airport with code '%s' already exists in database" % airport.code)

        self._airports.append(airport)
        self._mapping[airport.code] = airport

    def get_airport(self, code, graceful=False):
        """Retrieve airport by its code from database

        :param code: code of airport to be retrieved
        :param graceful: if true do not raise an exception but return None if no airport found
        :return: Airport
        :raises KeyError: if no airport was found
        """
        _logger.debug("Retrieving airport with code '%s' from airport database", code)

        ret = self._mapping.get(code)

        if ret is None and not graceful:
            raise KeyError("Airport with code '%s' not found in the database" % code)

        return ret

    def get_airport_or_create(self, code):
        """Retrieve airport from database, if does not exist create it

        :param code: airport code
        :return: airport instance
        :rtype: Airport
        """
        ret = self.get_airport(code, graceful=True)

        if ret is None:
            ret = Airport(code)
            self.register(ret)

        return ret
