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

_logger = logging.getLogger(__name__)


class FlightDatabase(object):
    """In-memory database holding info about flights"""
    def __init__(self, flights=None):
        """
        :param flights: a list of flights stored in database
        :type flights: list(Flight)
        """
        self._flights = flights or []
        self._mapping = {}

        for flight in self.flights:
            if flight.flight_number in self._mapping:
                raise ValueError("Multiple flights with same number provided, "
                                 "number %s" % flight.flight_number)
            self._mapping[flight.flight_number] = flight

    @property
    def flights(self):
        """
        :return: all available flights in database
        """
        return self._flights

    def __str__(self):
        return str(list(self._mapping.keys()))

    def to_csv(self):
        """
        :return: a CSV representation of flight database
        """
        header = "source,destination,departure,arrival,flight_number,price," \
                 "bags_allowed,bag_price\n"
        return header + "".join(f.to_csv() for f in self.flights)

    def to_dict(self):
        """
        :return: a dict representation of flight database
        """
        return {'flights': [f.to_dict() for f in self._flights]}

    def register(self, flight):
        """Register flight to database

        :param flight: flight to be registered
        :type flight: Flight
        :raises ValueError: if flight already exists in database
        """
        _logger.debug("Registering flight '%s' to flight database", flight.flight_number)

        if flight.flight_number in self._mapping:
            raise ValueError("Flight with number '%s' is already in database"
                             % flight.flight_number)

        self.flights.append(flight)
        self._mapping[flight.flight_number] = flight
