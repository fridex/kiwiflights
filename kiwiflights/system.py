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
"""A module where the whole power sits"""

import logging
import datetime
from copy import copy
from dateutil import parser as datetime_parser
from .flight import Flight
from .airport_database import AirportDatabase
from .flight_database import FlightDatabase
from .itinerary import Itinerary

_logger = logging.getLogger(__name__)


class System(object):
    """Main system entry-point"""

    # Defaults for wait window to limit customer wait time at airports
    # XXX: this could be propagated from CLI to parametrize user needs, keep this simple now
    _DEFAULT_MAX_WAIT_TIME = datetime.timedelta(hours=4)
    _DEFAULT_MIN_WAIT_TIME = datetime.timedelta(hours=1)

    # CSV indexes
    _CSV_IDX_SOURCE = 0
    _CSV_IDX_DESTINATION = 1
    _CSV_IDX_DEPARTURE = 2
    _CSV_IDX_ARRIVAL = 3
    _CSV_IDX_FLIGHT_NUMBER = 4
    _CSV_IDX_PRICE = 5
    _CSV_IDX_BAGS_ALLOWED = 6
    _CSV_IDX_BAG_PRICE = 7
    _CSV_ITEM_COUNT = 8

    def __init__(self, flight_database=None, airport_database=None):
        """
        :param flight_database: flight database to be used, defaults to FlightDatabase
        :param airport_database: airport database to be used, defaults to AirportDatabase
        """
        self.flight_database = flight_database or FlightDatabase()
        self.airport_database = airport_database or AirportDatabase()

    def __repr__(self):
        return "System(flight_database=%s, airport_database=%s)"\
               % (self.flight_database, self.airport_database)

    def _get_initialized_stack(self):
        """Get freshly initialized stack item

        :return: stack (list) of Itineraries
        :rtype: list(Itineraries)
        """
        stack = []
        for airport in self.airport_database.airports:
            for departure in airport.departures:
                # We use frozenset to optimize checks for flights that were taken to (ideally) O(1)
                seen = frozenset((departure.source, departure.destination,))
                stack.append(Itinerary(price=departure.price,
                                       bags_allowed=departure.bags_allowed,
                                       bag_price=departure.bag_price,
                                       total_flight_duration=departure.get_duration(),
                                       total_wait_time=datetime.timedelta(0),
                                       segments_seen={seen: True},
                                       flights_taken=[departure]))
        return stack

    @staticmethod
    def _get_next_stack_item(prev_stack_item, next_flight):
        """Get next stack item

        :param prev_stack_item: previous stack item
        :type prev_stack_item: Itinerary
        :param next_flight: next flight based on which the next stack item should be computed
        :return: new stack item
        :rtype: Itinerary
        """
        prev_flight = prev_stack_item.flights_taken[-1]

        # Prevent from updating next items on stack
        new_total_duration = prev_stack_item.total_flight_duration + next_flight.get_duration()
        new_total_wait = prev_stack_item.total_wait_time \
            + (next_flight.departure - prev_flight.arrival)

        new_seen = copy(prev_stack_item.segments_seen)
        new_seen[frozenset((prev_flight.destination, next_flight.destination,))] = True

        return Itinerary(price=prev_stack_item.price + next_flight.price,
                         bags_allowed=min(prev_stack_item.bags_allowed, next_flight.bags_allowed),
                         bag_price=prev_stack_item.bag_price + next_flight.bag_price,
                         total_flight_duration=new_total_duration,
                         total_wait_time=new_total_wait,
                         flights_taken=prev_stack_item.flights_taken + [next_flight],
                         segments_seen=new_seen)

    @classmethod
    def _inside_wait_window(cls, prev_flight, next_flight):
        """Check whether waiting time is inside defined window

        :param prev_flight: previous flight that was taken
        :param next_flight: next flight that could be taken
        :return: True if waiting time resists in defined time window
        """
        wait_time = next_flight.departure - prev_flight.arrival
        return cls._DEFAULT_MIN_WAIT_TIME <= wait_time <= cls._DEFAULT_MAX_WAIT_TIME

    def compute_itineraries(self):
        """Compute itineraries

        :return: a list of available itineraries
        :rtype: list(Itineraries)
        """
        stack = self._get_initialized_stack()
        itineraries = []

        while stack:
            item = stack.pop()

            last_flight = item.flights_taken[-1]
            _logger.debug("Inspecting possibilities after flight %s, %d",
                          last_flight.flight_number, len(last_flight.destination.departures))
            for next_flight in last_flight.destination.departures:
                if not self._inside_wait_window(last_flight, next_flight):
                    _logger.debug("Next flight %s after flight %s does not fit inside window",
                                  next_flight, last_flight)
                    continue

                segment = frozenset((last_flight.destination, next_flight.destination,))
                if segment in item.segments_seen:
                    _logger.debug("Next flight %s after flight %s would cause cycle",
                                  next_flight, last_flight)
                    continue

                next_stack_item = self._get_next_stack_item(item, next_flight)
                _logger.debug("New itinerary computed: %s", next_stack_item)
                itineraries.append(next_stack_item)
                stack.append(next_stack_item)

        return itineraries

    @classmethod
    def from_csv_file(cls, file, has_header=True):
        """ Create database from a CSV file

        :param file: opened file-like object
        :param has_header: True if file has a header on the first line
        :return:system with parsed flights
        :rtype: System
        """
        # we could use csv module here, but keep it this way for now...
        system = System()
        line = file.readline()

        # skip a very first line - a CSV header
        if has_header:
            _logger.debug("Skipping CSV header: '%s'", line[:-1])  # remove \n
            line = file.readline()

        while line:
            _logger.debug("Parsing line: '%s'", line[:-1])  # remove \n
            items = line.split(',')

            if len(items) != cls._CSV_ITEM_COUNT:
                raise ValueError("Expected %d items in CVS file in file, got %d instead: %s"
                                 % (cls._CSV_ITEM_COUNT, len(items), str(items)))

            try:
                departure_datetime = datetime_parser.parse(items[cls._CSV_IDX_DEPARTURE])
            except ValueError:
                raise ValueError("Departure time '%s' is not correct"
                                 % items[cls._CSV_IDX_DEPARTURE])

            try:
                arrival_datetime = datetime_parser.parse(items[cls._CSV_IDX_ARRIVAL])
            except ValueError:
                raise ValueError("Arrival time '%s' is not correct" % items[cls._CSV_IDX_ARRIVAL])

            if departure_datetime >= arrival_datetime:
                raise ValueError("Departure after arrival detected, flight '%s'"
                                 % items[cls._CSV_IDX_FLIGHT_NUMBER])

            source_airport = system.airport_database. \
                get_airport_or_create(items[cls._CSV_IDX_SOURCE])
            destination_airport = system.airport_database. \
                get_airport_or_create(items[cls._CSV_IDX_DESTINATION])

            new_flight = Flight(
                source=source_airport,
                destination=destination_airport,
                departure=departure_datetime,
                arrival=arrival_datetime,
                flight_number=items[cls._CSV_IDX_FLIGHT_NUMBER],
                price=float(items[cls._CSV_IDX_PRICE]),
                bags_allowed=int(items[cls._CSV_IDX_BAGS_ALLOWED]),
                bag_price=float(items[cls._CSV_IDX_BAG_PRICE])
            )

            _logger.debug("New flight parsed: %s", new_flight)

            system.flight_database.register(new_flight)
            destination_airport.register_flight(new_flight)
            source_airport.register_flight(new_flight)
            line = file.readline()

        return system
