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
"""Airport representation"""


class Airport(object):
    """Airport representation"""
    def __init__(self, code):
        """
        :param code: airport unique code
        """
        self.code = code
        self.arrivals = []
        self.departures = []

    def __repr__(self):
        return "Airport(code='%s')" % self.code

    def to_dict(self):
        """
        :return: a dict representation of airport
        """
        return {
            "airport": self.code,
            "departures": [f.to_dict() for f in self.departures],
            "arrivals": [f.to_dict() for f in self.arrivals]
        }

    def register_flight(self, flight):
        """Register flight to airport

        :param flight: flight to be registered
        :return:
        """
        if flight.source == flight.destination:
            raise ValueError("Source and destination of provided flight '%s' is same: %s"
                             % (flight.flight_number, flight.source))

        if flight.source == self:
            self.departures.append(flight)
        elif flight.destination == self:
            self.arrivals.append(flight)
        else:
            raise ValueError("Cannot register flight to airport that is not listed "
                             "in departure nor arrival")
