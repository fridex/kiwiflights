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
"""Flight manipulation, representation and parsing"""

from .utils import datetime_format


class Flight(object):
    """Flight representation"""
    def __init__(self, **param):
        """
        :param opts: flight parameters, expected: source, destination, departure, arrival,
                     flight_number, price, bags_allowed, bag_price
        """
        self.source = param.pop('source')
        self.destination = param.pop('destination')
        self.departure = param.pop('departure')
        self.arrival = param.pop('arrival')
        self.flight_number = param.pop('flight_number')
        self.price = param.pop('price')
        self.bags_allowed = param.pop('bags_allowed')
        self.bag_price = param.pop('bag_price')

        if param:
            raise KeyError("Unknown flight attributes: %s" % str(param))

    def __repr__(self):
        return "Flight(source={source}, " \
                       "destination={destination}, " \
                       "departure='{departure}', " \
                       "arrival='{arrival}', " \
                       "flight_number='{flight_number}', " \
                       "price={price}, " \
                       "bags_allowed={bags_allowed}, " \
                       "bag_price={bag_price})".format(**self.__dict__)

    def get_duration(self):
        """
        :return: raw flight duration
        :rtype: datetime.timedelta
        """
        return self.arrival - self.departure

    def to_csv(self):
        """
        :return: CSV interpretation of the flight
        """
        return ",".join((str(self.source),
                         str(self.destination),
                         datetime_format(self.departure),
                         datetime_format(self.arrival),
                         self.flight_number,
                         self.price,
                         self.bags_allowed,
                         self.bag_price,))

    def to_dict(self):
        """
        :return: dict representation if the flight
        """
        return {
            'source': self.source.code,
            'destination': self.destination.code,
            'departure': datetime_format(self.departure),
            'arrival': datetime_format(self.arrival),
            'flight_number': self.flight_number,
            'price': self.price,
            'bags_allowed': self.bags_allowed,
            'bag_price': self.bag_price
        }
