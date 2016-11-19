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
"""Itinerary representation"""


class Itinerary(object):
    """Itinerary representation"""
    def __init__(self, **attributes):
        """
        :param attributes: itinerary attributes
        """
        self.price = attributes.pop('price')
        self.bags_allowed = attributes.pop('bags_allowed')
        self.bag_price = attributes.pop('bag_price')
        self.total_flight_duration = attributes.pop('total_flight_duration')
        self.total_wait_time = attributes.pop('total_wait_time')
        self.segments_seen = attributes.pop('segments_seen')
        self.flights_taken = attributes.pop('flights_taken')

    def __repr__(self):
        return "Itinerary(price={price}, " \
                         "bags_allowed={bags_allowed}, " \
                         "bag_price={bag_price}, " \
                         "total_flight_duration={total_flight_duration}, " \
                         "total_wait_time={total_wait_time}, " \
                         "flights_taken={flights_taken}, " \
                         "segments_seen={segments_seen})".format(**self.__dict__)

    def to_dict(self):
        """
        :return: dict representation of itinerary
        """
        stops = [{
            "airport": f.destination.code,
            "wait_time": str(self.flights_taken[idx+1].departure - self.flights_taken[idx].arrival)
        } for idx, f in enumerate(self.flights_taken[:-1])]

        return {
            'price': self.price,
            'bags_allowed': self.bags_allowed,
            'bag_price': self.bag_price,
            'total_flight_duration': str(self.total_flight_duration),
            'total_wait_time': str(self.total_wait_time),
            'flights_taken': [f.flight_number for f in self.flights_taken],
            'source': self.flights_taken[0].source.code,
            'destination': self.flights_taken[-1].destination.code,
            'stops': stops,
        }
